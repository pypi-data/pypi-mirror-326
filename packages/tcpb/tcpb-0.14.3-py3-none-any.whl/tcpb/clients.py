"""Python clients for communicating with TeraChem in Server Mode.

Two clients exist, one for communicating directly with the protocol buffer server run
by TeraChem. One for communicating with the TeraChem Frontend server which provides
increased functionality.

Note that Stefan Seritan has implemented a small protocol on top of the
protobufs since we send them in binary over TCP ALL MESSAGES ARE REQUIRED TO
HAVE AN 8 BYTE HEADER
First 4 bytes: int32 of protocol buffer message type (check the MessageType enum
in the protobuf file)
Second 4 bytes: int32 of packet size (not including the header)
"""

import logging
import socket
import struct
import traceback
from time import sleep
from typing import Dict, List, Optional, Union
from uuid import uuid4

import httpx
import numpy as np
from google.protobuf.json_format import MessageToDict
from qcio import ProgramInput, ProgramOutput, Provenance

from tcpb.utils import (  # job_output_to_atomic_result,
    prog_inp_to_job_inp,
    to_single_point_results,
)

# Import the Protobuf messages generated from the .proto file
from . import terachem_server_pb2 as pb
from .config import settings
from .exceptions import ServerError

logger = logging.getLogger(__name__)


class TCProtobufClient:
    """Connect and communicate with a TeraChem instance running in Protocol Buffer server mode
    (i.e. TeraChem was started with the -s|--server flag)
    """

    program = "terachem-pbs"

    def __init__(
        self,
        host: str = settings.tcpb_host,
        port: int = settings.tcpb_port,
        debug=False,
        trace=False,
    ):
        """Initialize a TCProtobufClient object.

        Parameters:
            host: Hostname
            port: Port number (must be above 1023)
            debug: If True, assumes connections work (used for testing with no server)
            trace: If True, packets are saved to .bin files (which can then be used for testing)
        """
        if port < 1023:
            raise ValueError(
                "Port number is not allowed to below 1023 (system reserved ports)"
            )
        self.host = host
        self.port = port
        self.debug = debug
        self.trace = trace
        if self.trace:
            self.intracefile = open("client_recv.bin", "wb")
            self.outtracefile = open("client_sent.bin", "wb")

        self.tcsock = None
        # Would like to not hard code this, but the truth is I am expecting exactly 8 bytes, not whatever Python thinks 2 ints is
        self.header_size = 8

        self.prev_results = None

        self.curr_job_dir: Optional[str] = None
        self.curr_job_scr_dir: Optional[str] = None
        self.curr_job_id: Optional[int] = None

    def __enter__(self):
        """
        Allow automatic context management using 'with' statement

        >>> with TCProtobufClient(host, port, **options) as TC:
        >>>     E = TC.compute_energy(geom)
        """
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        """
        Disconnect in automatic context management.
        """
        self.disconnect()

    def connect(self):
        """Connect to the TeraChem Protobuf server"""
        if self.debug:
            logging.info("in debug mode - assume connection established")
            return

        try:
            self.tcsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcsock.settimeout(10.0)  # Timeout of 10 seconds
            self.tcsock.connect((self.host, self.port))
        except socket.error as msg:
            raise ServerError(f"Problem connecting to server: {msg}", self)

    def disconnect(self):
        """Disconnect from the TeraChem Protobuf server"""
        if self.debug:
            logging.info("in debug mode - assume disconnection worked")
            return

        try:
            self.tcsock.shutdown(2)  # Shutdown read and write
            self.tcsock.close()
            self.tcsock = None
        except socket.error as msg:
            logger.error(
                f"Problem communicating with server: {msg}. Disconnect assumed to have happened"
            )

    def is_available(self):
        """Asks the TeraChem Protobuf server whether it is available or busy through the Status protobuf message.
        Note that this does not reserve the server, and the status could change after this function is called.

        Returns:
            bool: True if the TeraChem PB server is currently available (no running job)
        """
        if self.debug:
            logging.info("in debug mode - assume terachem server is available")
            return True

        # Send Status message
        self._send_msg(pb.STATUS, None)

        # Receive Status header
        status = self._recv_msg(pb.STATUS)

        return not status.busy

    def compute(
        self, inp_data: ProgramInput, raise_exc: bool = True, **kwargs
    ) -> ProgramOutput:
        """Top level method for performing computations with QCSchema inputs/outputs

        Args:
            inp_data: AtomicInput object
            raise_exc: If True, raise an error if the computation fails

        Returns:
            ProgramOutput object
        """
        # Create protobuf message
        job_input_msg = prog_inp_to_job_inp(inp_data)
        try:
            # Send message to server; retry until accepted
            accepted = False
            retries = 0
            while not accepted:
                self._send_msg(pb.JOBINPUT, job_input_msg)
                status = self._recv_msg(pb.STATUS)
                self._set_status(status)
                accepted = status.accepted
                if not accepted:
                    retries += 1
                    if retries > 10:
                        raise ServerError("Server is busy and not accepting jobs", self)
                    sleep(0.5)
            while not self.check_job_complete():
                sleep(0.25)
            # Collect output from server
            job_output = self._recv_msg(pb.JOBOUTPUT)
        except ServerError as e:
            # Server likely crashed due to calculation failing
            prog_output: ProgramOutput = ProgramOutput(
                input_data=inp_data,
                success=False,
                traceback=traceback.format_exc(),
                results={},
                provenance=Provenance(
                    program=self.program,
                    scratch_dir=self.curr_job_dir,
                ),
            )
            e.program_output = prog_output
            if raise_exc:
                raise e
            else:
                return prog_output
        else:
            return self.job_output_to_atomic_result(
                inp_data=inp_data, job_output=job_output
            )

    def job_output_to_atomic_result(
        self,
        *,
        inp_data: ProgramInput,
        job_output: pb.JobOutput,
    ) -> ProgramOutput:
        """Convert JobOutput to ProgramOutput"""
        # Convert job_output to python types
        # NOTE: Required so that ProgramOutput is JSON serializable. Protobuf types are not.
        jo_dict = MessageToDict(job_output, preserving_proto_field_name=True)

        # Create ProgramOutput
        prog_output: ProgramOutput = ProgramOutput(
            input_data=inp_data,
            success=True,
            provenance=Provenance(
                program=self.program, scratch_dir=jo_dict.get("job_dir")
            ),
            results=to_single_point_results(job_output),
        )
        # And extend extras to include values additional to input extras
        prog_output.results.extras.update(
            {
                "charges": jo_dict.get("charges"),
                "spins": jo_dict.get("spins"),
                "meyer_bond_order": jo_dict.get("bond_order"),
                "orb_size": jo_dict.get("orb_size"),
                "excited_state_energies": jo_dict.get("energy"),
                "cis_transition_dipoles": jo_dict.get("cis_transition_dipoles"),
                "compressed_bond_order": jo_dict.get("compressed_bond_order"),
                "compressed_hessian": jo_dict.get("compressed_hessian"),
                "compressed_ao_data": jo_dict.get("compressed_ao_data"),
                "compressed_primitive_data": jo_dict.get("compressed_primitive_data"),
                "compressed_mo_vector": jo_dict.get("compressed_mo_vector"),
                "imd_mmatom_gradient": jo_dict.get("imd_mmatom_gradient"),
                "job_dir_scr": jo_dict.get("job_scr_dir"),
                "server_job_id": jo_dict.get("server_job_id"),
                "orb1afile": jo_dict.get("orb1afile"),
                "orb1bfile": jo_dict.get("orb1bfile"),
            }
        )

        return prog_output

    def send_job_async(self, jobType="energy", geom=None, unitType="bohr", **kwargs):
        """Pack and send the current JobInput to the TeraChem Protobuf server asynchronously.
        This function expects a Status message back that either tells us whether the job was accepted.

        Args:
            jobType:    Job type key, as defined in the pb.JobInput.RunType enum (defaults to "energy")
            geom:       Cartesian geometry of the new point
            unitType:   Unit type key, as defined in the pb.Mol.UnitType enum (defaults to "bohr")
            **kwargs:   Additional TeraChem keywords, check _process_kwargs for behaviour

        Returns:
            bool: True on job acceptance, False on server busy, and errors out if communication fails
        """
        if jobType.upper() not in list(pb.JobInput.RunType.keys()):
            raise ValueError(
                "Job type specified is not available in this version of the TCPB client\n"
                "Allowed run types: {}".format(list(pb.JobInput.RunType.keys()))
            )
        if geom is None:
            raise SyntaxError("Did not provide geometry to send_job_async()")
        if isinstance(geom, np.ndarray):
            geom = geom.flatten()
        if unitType.upper() not in list(pb.Mol.UnitType.keys()):
            raise ValueError(
                "Unit type specified is not available in this version of the TCPB client\n"
                "Allowed unit types: {}".format(list(pb.Mol.UnitType.keys()))
            )

        if self.debug:
            logging.info("in debug mode - assume job completed")
            return True

        # Job setup
        job_input_msg = self._create_job_input_msg(jobType, geom, unitType, **kwargs)

        self._send_msg(pb.JOBINPUT, job_input_msg)

        status_msg = self._recv_msg(pb.STATUS)

        if status_msg.WhichOneof("job_status") == "accepted":
            self._set_status(status_msg)

            return True
        else:
            return False

    def _set_status(self, status_msg: pb.Status):
        """Sets status on self if job is accepted"""
        self.curr_job_dir = status_msg.job_dir
        self.curr_job_scr_dir = status_msg.job_scr_dir
        self.curr_job_id = status_msg.server_job_id

    def _create_job_input_msg(self, jobType, geom, unitType="bohr", **kwargs):
        """Method for setting up jobs according to old mechanism

        Refactored this method out to allow for better testing
        """
        job_input_msg = pb.JobInput()
        job_input_msg.run = pb.JobInput.RunType.Value(jobType.upper())
        job_input_msg.mol.xyz.extend(geom)
        job_input_msg.mol.units = pb.Mol.UnitType.Value(unitType.upper())

        self._process_kwargs(job_input_msg, **kwargs)
        return job_input_msg

    def check_job_complete(self):
        """Pack and send a Status message to the TeraChem Protobuf server asynchronously.
        This function expects a Status message back with either working or completed set.
        Errors out if just busy message returned, implying the job we are checking was not submitted
        or had some other issue

        Returns:
            bool: True if job is completed, False otherwise
        """
        if self.debug:
            logging.info("in debug mode - assume check_job_complete is True")
            return True

        # Send Status
        self._send_msg(pb.STATUS, None)

        # Receive Status
        status = self._recv_msg(pb.STATUS)

        if status.WhichOneof("job_status") == "completed":
            return True
        elif status.WhichOneof("job_status") == "working":
            return False
        else:
            raise ServerError(
                "Invalid or no job status received, either no job submitted before check_job_complete() or major server issue",
                self,
            )

    def recv_job_async(self):
        """Recv and unpack a JobOutput message from the TeraChem Protobuf server asynchronously.
        This function expects the job to be ready (i.e. check_job_complete() returned true),
        so will error out on timeout.

        Creates a results dictionary that mirrors the JobOutput message, using NumPy arrays when appropriate.
        Results are also saved in the prev_results class member.
        An inclusive list of the results members (with types):

        * atoms:              Flat # of atoms NumPy array of 2-character strings
        * geom:               # of atoms by 3 NumPy array of doubles
        * energy:             Either empty, single energy, or flat # of cas_energy_labels of NumPy array of doubles
        * charges:            Flat # of atoms NumPy array of doubles
        * spins:              Flat # of atoms NumPy array of doubles
        * dipole_moment:      Single element (units Debye)
        * dipole_vector:      Flat 3-element NumPy array of doubles (units Debye)
        * job_dir:            String
        * job_scr_dir:        String
        * server_job_id:      Int
        * orbfile:            String (if restricted is True, otherwise not included)
        * orbfile_a:          String (if restricted is False, otherwise not included)
        * orbfile_b:          String (if restricted is False, otherwise not included)
        * orb_energies:       Flat # of orbitals NumPy array of doubles (if restricted is True, otherwise not included)
        * orb_occupations:    Flat # of orbitals NumPy array of doubles (if restricted is True, otherwise not included)
        * orb_energies_a:     Flat # of orbitals NumPy array of doubles (if restricted is False, otherwise not included)
        * orb_occupations_a:  Flat # of orbitals NumPy array of doubles (if restricted is False, otherwise not included)
        * orb_energies_b:     Flat # of orbitals NumPy array of doubles (if restricted is False, otherwise not included)
        * orb_occupations_b:  Flat # of orbitals NumPy array of doubles (if restricted is False, otherwise not included)

        Additional (optional) members of results:

        * bond_order:         # of atoms by # of atoms NumPy array of doubles

        Available per job type:

        * gradient:           # of atoms by 3 NumPy array of doubles (available for 'gradient' job)
        * nacme:              # of atoms by 3 NumPy array of doubles (available for 'coupling' job)
        * ci_overlap:         ci_overlap_size by ci_overlap_size NumPy array of doubles (available for 'ci_vec_overlap' job)

        Available for CAS jobs:

        * cas_energy_labels:  List of tuples of (state, multiplicity) corresponding to the energy list
        * cas_transition_dipole:  Flat 3-element NumPy array of doubles (available for 'coupling' job)

        Available for CIS jobs:

        * cis_states:         Number of excited states for reported properties
        * cis_unrelaxed_dipoles:    # of excited states list of flat 3-element NumPy arrays (default included with 'cis yes', or explicitly with 'cisunrelaxdipole yes', units a.u.)
        * cis_relaxed_dipoles:      # of excited states list of flat 3-element NumPy arrays (included with 'cisrelaxdipole yes', units a.u.)
        * cis_transition_dipoles:   # of excited state combinations (N(N-1)/2) list of flat 3-element NumPy arrays (default includeded with 'cis yes', or explicitly with 'cistransdipole yes', units a.u.)
                                    Order given lexically (e.g. 0->1, 0->2, 1->2 for 2 states)

        Returns:
            dict: Results as described above
        """
        output = self._recv_msg(pb.JOBOUTPUT)

        # Parse output into normal python dictionary
        results = {
            "atoms": np.array(output.mol.atoms, dtype="S2"),
            "geom": np.array(output.mol.xyz, dtype=np.float64).reshape(-1, 3),
            "charges": np.array(output.charges, dtype=np.float64),
            "spins": np.array(output.spins, dtype=np.float64),
            "dipole_moment": output.dipoles[3],
            "dipole_vector": np.array(output.dipoles[:3], dtype=np.float64),
            "job_dir": output.job_dir,
            "job_scr_dir": output.job_scr_dir,
            "server_job_id": output.server_job_id,
        }

        if len(output.energy):
            results["energy"] = output.energy[0]

        if output.mol.closed is True:
            results["orbfile"] = output.orb1afile

            results["orb_energies"] = np.array(output.orba_energies)
            results["orb_occupations"] = np.array(output.orba_occupations)
        else:
            results["orbfile_a"] = output.orb1afile
            results["orbfile_b"] = output.orb1bfile

            results["orb_energies_a"] = np.array(output.orba_energies)
            results["orb_occupations_a"] = np.array(output.orba_occupations)
            results["orb_energies_b"] = np.array(output.orbb_energies)
            results["orb_occupations_b"] = np.array(output.orbb_occupations)

        if len(output.gradient):
            results["gradient"] = np.array(output.gradient, dtype=np.float64).reshape(
                -1, 3
            )

        if len(output.nacme):
            results["nacme"] = np.array(output.nacme, dtype=np.float64).reshape(-1, 3)

        if len(output.cas_transition_dipole):
            results["cas_transition_dipole"] = np.array(
                output.cas_transition_dipole, dtype=np.float64
            )

        if len(output.cas_energy_states):
            results["energy"] = np.array(
                output.energy[: len(output.cas_energy_states)], dtype=np.float64
            )
            results["cas_energy_labels"] = list(
                zip(output.cas_energy_states, output.cas_energy_mults)
            )

        if len(output.bond_order):
            nAtoms = len(output.mol.atoms)
            results["bond_order"] = np.array(
                output.bond_order, dtype=np.float64
            ).reshape(nAtoms, nAtoms)

        if len(output.ci_overlaps):
            results["ci_overlap"] = np.array(
                output.ci_overlaps, dtype=np.float64
            ).reshape(output.ci_overlap_size, output.ci_overlap_size)

        if output.cis_states > 0:
            results["energy"] = np.array(
                output.energy[: output.cis_states + 1], dtype=np.float64
            )
            results["cis_states"] = output.cis_states

            if len(output.cis_unrelaxed_dipoles):
                uDips = []
                for i in range(output.cis_states):
                    uDips.append(
                        np.array(
                            output.cis_unrelaxed_dipoles[4 * i : 4 * i + 3],
                            dtype=np.float64,
                        )
                    )
                results["cis_unrelaxed_dipoles"] = uDips

            if len(output.cis_relaxed_dipoles):
                rDips = []
                for i in range(output.cis_states):
                    rDips.append(
                        np.array(
                            output.cis_relaxed_dipoles[4 * i : 4 * i + 3],
                            dtype=np.float64,
                        )
                    )
                results["cis_relaxed_dipoles"] = rDips

            if len(output.cis_transition_dipoles):
                tDips = []
                for i in range(int((output.cis_states + 1) * output.cis_states / 2)):
                    tDips.append(
                        np.array(
                            output.cis_transition_dipoles[4 * i : 4 * i + 3],
                            dtype=np.float64,
                        )
                    )
                results["cis_transition_dipoles"] = tDips

        # Save results for user access later
        self.prev_results = results

        # Wipe state
        self.curr_job_dir = None
        self.curr_job_scr_dir = None
        self.curr_job_id = None

        return results

    def compute_job_sync(self, jobType="energy", geom=None, unitType="bohr", **kwargs):
        """Wrapper for send_job_async() and recv_job_async(), using check_job_complete() to poll the server.

        Args:
            jobType:    Job type key, as defined in the pb.JobInput.RunType enum (defaults to 'energy')
            geom:       Cartesian geometry of the new point
            unitType:   Unit type key, as defined in the pb.Mol.UnitType enum (defaults to 'bohr')
            **kwargs:   Additional TeraChem keywords, check _process_kwargs for behaviour

        Returns:
            dict: Results mirroring recv_job_async
        """
        if self.debug:
            logging.info(
                "in debug mode - assume compute_job_sync completed successfully"
            )
            return True

        accepted = self.send_job_async(jobType, geom, unitType, **kwargs)
        while accepted is False:
            sleep(0.5)
            accepted = self.send_job_async(jobType, geom, unitType, **kwargs)

        completed = self.check_job_complete()
        while completed is False:
            sleep(0.5)
            completed = self.check_job_complete()

        return self.recv_job_async()

    # CONVENIENCE FUNCTIONS #
    def compute_energy(self, geom=None, unitType="bohr", **kwargs):
        """Compute energy of a new geometry, but with the same atom labels/charge/spin
        multiplicity and wave function format as the previous calculation.

        Args:
            geom:       Cartesian geometry of the new point
            unitType:   Unit type key, as defined in the pb.Mol.UnitType enum (defaults to 'bohr')
            **kwargs:   Additional TeraChem keywords, check _process_kwargs for behaviour

        Returns:
            float: Energy
        """
        results = self.compute_job_sync("energy", geom, unitType, **kwargs)
        return results["energy"]

    def compute_gradient(self, geom=None, unitType="bohr", **kwargs):
        """Compute gradient of a new geometry, but with the same atom labels/charge/spin
        multiplicity and wave function format as the previous calculation.

        Args:
            geom:       Cartesian geometry of the new point
            unitType:   Unit type key, as defined in the pb.Mol.UnitType enum (defaults to 'bohr')
            **kwargs:   Additional TeraChem keywords, check _process_kwargs for behaviour

        Returns:
            tuple: Tuple of (energy, gradient)
        """
        results = self.compute_job_sync("gradient", geom, unitType, **kwargs)
        return results["energy"], results["gradient"]

    # Convenience to maintain compatibility with NanoReactor2
    def compute_forces(self, geom=None, unitType="bohr", **kwargs):
        """Compute forces of a new geometry, but with the same atoms labels/charge/spin
        multiplicity and wave function format as the previous calculation.

        Args:
            geom:       Cartesian geometry of the new point
            unitType:   Unit type key, as defined in the pb.Mol.UnitType enum (defaults to 'bohr')
            **kwargs:   Additional TeraChem keywords, check _process_kwargs for behaviour

        Returns:
            tuple: Tuple of (energy, forces), which is really (energy, -gradient)
        """
        results = self.compute_job_sync("gradient", geom, unitType, **kwargs)
        return results["energy"], -1.0 * results["gradient"]

    def compute_coupling(self, geom=None, unitType="bohr", **kwargs):
        """Compute nonadiabatic coupling of a new geometry, but with the same atoms labels/charge/spin
        multiplicity and wave function format as the previous calculation.

        Args:
            geom:       Cartesian geometry of the new point
            unitType:   Unit type key, as defined in the pb.Mol.UnitType enum (defaults to 'bohr')
            **kwargs:   Additional TeraChem keywords, check _process_kwargs for behaviour

        Returns:
            (num_atoms, 3) ndarray: Nonadiabatic coupling vector
        """
        results = self.compute_job_sync("coupling", geom, unitType, **kwargs)
        return results["nacme"]

    def compute_ci_overlap(
        self,
        geom=None,
        geom2=None,
        cvec1file=None,
        cvec2file=None,
        orb1afile=None,
        orb1bfile=None,
        orb2afile=None,
        orb2bfile=None,
        unitType="bohr",
        **kwargs,
    ):
        """Compute wavefunction overlap given two different geometries, CI vectors, and orbitals,
        using the same atom labels/charge/spin multiplicity as the previous calculation.

        To run a closed shell calculation, only populate orb1afile/orb2afile, leaving orb1bfile/orb2bfile blank.
        Currently, open-shell overlap calculations are not supported by TeraChem.

        Args:
            geom:       Cartesian geometry of the first point
            geom2:      Cartesian geometry of the second point
            cvec1file:  Binary file of CI vector for first geometry (row-major, double64)
            cvec2file:  Binary file of CI vector for second geometry (row-major, double64)
            orb1afile:  Binary file of alpha MO coefficients for first geometry (row-major, double64)
            orb1bfile:  Binary file of beta MO coefficients for first geometry (row-major, double64)
            orb2afile:  Binary file of alpha MO coefficients for second geometry (row-major, double64)
            orb2bfile:  Binary file of beta MO coefficients for second geometry (row-major, double64)
            unitType:   Unit type key, as defined in the pb.Mol.UnitType enum (defaults to 'bohr')
            **kwargs:   Additional TeraChem keywords, check _process_kwargs for behaviour

        Returns:
            (num_states, num_states) ndarray: CI vector overlaps
        """
        if geom is None or geom2 is None:
            raise SyntaxError("Did not provide two geometries to compute_ci_overlap()")
        if cvec1file is None or cvec2file is None:
            raise SyntaxError("Did not provide two CI vectors to compute_ci_overlap()")
        if orb1afile is None or orb1bfile is None:
            raise SyntaxError(
                "Did not provide two sets of orbitals to compute_ci_overlap()"
            )
        if (
            (orb1bfile is not None and orb2bfile is None)
            or (orb1bfile is None and orb2bfile is not None)
            and kwargs["closed_shell"] is False
        ):
            raise SyntaxError(
                "Did not provide two sets of open-shell orbitals to compute_ci_overlap()"
            )
        elif (
            orb1bfile is not None
            and orb2bfile is not None
            and kwargs["closed_shell"] is True
        ):
            print(
                "WARNING: System specified as closed, but open-shell orbitals were passed to compute_ci_overlap(). Ignoring beta orbitals."
            )

        if kwargs["closed_shell"]:
            results = self.compute_job_sync(
                "ci_vec_overlap",
                geom,
                unitType,
                geom2=geom2,
                cvec1file=cvec1file,
                cvec2file=cvec2file,
                orb1afile=orb1afile,
                orb2afile=orb2afile,
                **kwargs,
            )
        else:
            raise RuntimeError(
                "WARNING: Open-shell systems are currently not supported for overlaps"
            )
            # results = self.compute_job_sync("ci_vec_overlap", geom, unitType, geom2=geom2,
            #    cvec1file=cvec1file, cvec2file=cvec2file,
            #    orb1afile=orb1afile, orb1bfile=orb1bfile,
            #    orb2afile=orb1bfile, orb2bfile=orb2bfile, **kwargs)

        return results["ci_overlap"]

    # Private kwarg helper function
    def _process_kwargs(self, job_options, **kwargs):  # noqa NOTE: C901 too complex!
        """Process user-provided keyword arguments into a JobInput object

        Several keywords are processed by the client to set more complex fields
        in the Protobuf messages. These are:

        * geom:               Sets job_options.mol.xyz from a list or NumPy array
        * geom2:              Sets job_options.xyz2 from a list or NumPy array
        * bond_order:         Sets job_options.return_bond_order to True or False

        All others are passed through as key-value pairs to the server, which will
        place them in the start file.
        Passing None to a previously set option will remove it from job_options

        Args:
            job_options: Target JobInput object
            **kwargs: Keyword arguments passed by user
        """
        # Validate all options are here
        # TODO: Replace with mtzutils.Options
        required = [
            "atoms",
            "charge",
            "spinmult",
            "closed_shell",
            "restricted",
            "method",
            "basis",
        ]
        types = [str, int, int, bool, bool, str, str]

        for r, t in zip(required, types):
            if kwargs.get(r, None) is None:
                raise SyntaxError("Keyword %s must be specified in options" % r)
            elif r == "atoms":
                for a in kwargs["atoms"]:
                    if not isinstance(a, t):
                        raise TypeError("Each atom must have type: basestring")
            elif r == "method":
                if not isinstance(kwargs["method"], t):
                    raise TypeError("%s must have type: %s" % (r, t))
                elif kwargs["method"].upper() not in list(
                    pb.JobInput.MethodType.keys()
                ):
                    raise ValueError(
                        "Method specified is not available in this version of the TCPB client\n"
                        "Allowed methods: {}".format(
                            list(pb.JobInput.MethodType.keys())
                        )
                    )
            elif not isinstance(kwargs[r], t):
                raise TypeError("%s must have type: %s" % (r, t))

        for key, value in kwargs.items():
            if key == "atoms":
                job_options.mol.atoms.extend(value)
            elif key == "charge":
                job_options.mol.charge = value
            elif key == "spinmult":
                job_options.mol.multiplicity = value
            elif key == "closed_shell":
                job_options.mol.closed = value
            elif key == "restricted":
                job_options.mol.restricted = value
            elif key == "method":
                job_options.method = pb.JobInput.MethodType.Value(value.upper())
            elif key == "basis":
                job_options.basis = value
            elif key == "geom":
                # Standard geometry, usually handled in other calling functions but here just in case
                if isinstance(value, np.ndarray):
                    value = value.flatten()
                if len(kwargs["atoms"]) != len(value) / 3.0:
                    raise ValueError(
                        "Geometry provided to geom does not match atom list"
                    )

                del job_options.mol.xyz[:]
                job_options.mol.xyz.extend(value)
            elif key == "geom2":
                # Second geometry for ci_vec_overlap job
                if isinstance(value, np.ndarray):
                    value = value.flatten()
                if len(kwargs["atoms"]) != len(value) / 3.0:
                    raise ValueError(
                        "Geometry provided to geom2 does not match atom list"
                    )

                del job_options.xyz2[:]
                job_options.xyz2.extend(value)
            elif key == "bond_order":
                # Request Meyer bond order matrix
                if value is not True and value is not False:
                    raise ValueError("Bond order request must be True or False")

                job_options.return_bond_order = value
            elif key == "mo_output":
                # Request AO and MO information
                if value is True:
                    job_options.imd_orbital_type = pb.JobInput.ImdOrbitalType.Value(
                        "WHOLE_C"
                    )
            elif key in job_options.user_options:
                # Overwrite currently defined custom user option
                index = job_options.user_options.index(key)
                if value is None:
                    del job_options.user_options[index : (index + 1)]
                else:
                    job_options.user_options[index + 1] = str(value)
            elif key not in job_options.user_options and value is not None:
                # New custom user option
                job_options.user_options.extend([key, str(value)])

    # Private send/recv functions
    def _send_msg(self, msg_type, msg_pb=None):
        """Sends a header + PB to the TeraChem Protobuf server (must be connected)

        Args:
            msg_type: Message type (defined as enum in protocol buffer)
            msg_pb: Protocol Buffer to send to the TCPB server
        """
        # This will always pack integers as 4 bytes since I am requesting a standard packing (big endian)
        # Big endian is convention for network byte order (because IBM or someone)
        if msg_pb is None:
            msg_size = 0
        else:
            msg_size = msg_pb.ByteSize()

        header = struct.pack(">II", msg_type, msg_size)
        try:
            self.tcsock.sendall(header)
        except socket.error as msg:
            raise ServerError("Could not send header: {}".format(msg), self)

        msg_str = b""
        if msg_pb is not None:
            try:
                msg_str = msg_pb.SerializeToString()
                self.tcsock.sendall(msg_str)
            except socket.error as msg:
                raise ServerError("Could not send protobuf: {}".format(msg), self)

        if self.trace:
            packet = header + msg_str
            self.outtracefile.write(packet)

    def _recv_msg(self, msg_type):  # noqa NOTE: C901 too complex!
        """Receives a header + PB from the TeraChem Protobuf server (must be connected)

        Args:
            msg_type: Expected message type (defined as enum in protocol buffer)

        Returns:
            protobuf: Protocol Buffer of type msg_type (or None if no PB was sent)
        """
        # Receive header
        try:
            header = b""
            nleft = self.header_size
            while nleft:
                data = self.tcsock.recv(nleft)
                if data == b"":
                    break
                header += data
                nleft -= len(data)

            # Check we got full message
            if nleft == self.header_size and data == b"":
                raise ServerError(
                    "Could not recv header because socket was closed from server", self
                )
            elif nleft:
                raise ServerError(
                    "Recv'd {} of {} expected bytes for header".format(
                        nleft, self.header_size
                    ),
                    self,
                )
        except socket.error as msg:
            raise ServerError("Could not recv header: {}".format(msg), self)

        msg_info = struct.unpack_from(">II", header)

        if msg_info[0] != msg_type:
            raise ServerError(
                "Received header for incorrect packet type (expecting {} and got {})".format(
                    msg_type, msg_info[0]
                ),
                self,
            )

        # Receive Protocol Buffer (if one was sent)
        if msg_info[1] >= 0:
            try:
                msg_str = b""
                nleft = msg_info[1]
                while nleft:
                    data = self.tcsock.recv(nleft)
                    if data == b"":
                        break
                    msg_str += data
                    nleft -= len(data)

                # Check we got full message
                if nleft == self.header_size and data == b"":
                    raise ServerError(
                        "Could not recv message because socket was closed from server",
                        self,
                    )
                elif nleft:
                    raise ServerError(
                        "Recv'd {} of {} expected bytes for protobuf".format(
                            nleft, msg_info[1]
                        ),
                        self,
                    )
            except socket.error as msg:
                raise ServerError("Could not recv protobuf: {}".format(msg), self)

        if msg_type == pb.STATUS:
            recv_pb = pb.Status()
        elif msg_type == pb.MOL:
            recv_pb = pb.Mol()
        elif msg_type == pb.JOBINPUT:
            recv_pb = pb.JobInput()
        elif msg_type == pb.JOBOUTPUT:
            recv_pb = pb.JobOutput()
        else:
            raise ServerError(
                "Unknown message type {} for received message.".format(msg_type), self
            )

        recv_pb.ParseFromString(msg_str)

        if self.trace:
            packet = header + msg_str
            self.intracefile.write(packet)

        return recv_pb


class TCFrontEndClient(TCProtobufClient):
    """Client for interacting with TeraChem FrontEnd.

    TeraChemFrontEndClient communicates with a TeraChem Protocol Buffer Server for
    QC compute jobs and with a file server to get/put files to the server. A file may
    be put to the server e.g., to use as an initial wave function guess, or any output
    file retrieved after a computation.
    """

    program = "terachem-fe"

    def __init__(
        self,
        host: str = settings.tcpb_host,
        port: int = settings.tcpb_port,
        frontend_host: str = settings.tcpb_frontend_host,
        frontend_port: int = settings.tcpb_frontend_port,
        uploads_prefix: str = "uploads",
        debug=False,
        trace=False,
    ):
        self.frontend_host = frontend_host
        self.frontend_port = frontend_port
        self.uploads_prefix = uploads_prefix

        super().__init__(host, port, debug, trace)

    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Main method for sending requests to the TCFrontEnd file server"""

        with httpx.Client() as client:
            res = client.request(
                method.upper(),
                f"http://{self.frontend_host}:{self.frontend_port}/{path}",
                **kwargs,
            )
        res.raise_for_status()
        return res

    def _try_delete(self, path: str) -> None:
        """Try to delete a file, do not raise exception if file not found"""
        try:
            self._request("DELETE", f"{path}")
        except httpx.HTTPStatusError:
            logger.error(f"Could not delete file at path: '{path}'")

    def ls(self, path: str = "/") -> List[Dict[str, str]]:
        """List directories on TeraChem Server

        Parameters:
            path: Optional filepath.
        """
        if not path.endswith("/"):
            path += "/"

        req = self._request("GET", path)
        return req.json()

    def get(self, path: str) -> bytes:
        """Retrieve file from TeraChem Server

        Parameters:
            path: Full filepath to the file to download. Does not begin with '/'.

        Returns:
            Bytes of the file. All files (text or binary) returned as bytes. So to
            write to disk open file in binary mode. e.g.,:
                with open('my_output.txt', 'wb') as f:
                    f.write(client.get('path_to_file'))
        """
        req = self._request("GET", path)
        return req.content

    def put(self, filename: str, content: bytes) -> str:
        """Upload a file to the TeraChem Server

        Returns:
            Path to the uploaded file.
            NOTE: Full path will vary from filename passed as server will place file
                into designated uploads directory with uuid in path.
        """
        uuid = uuid4()
        req = self._request(
            "PUT", f"{self.uploads_prefix}/{uuid}-{filename}", content=content
        )
        return str(req.url.path)[1:]  # remove initial '/'

    def delete(self, path_or_filename: str) -> None:
        """Delete a directory or file from the TeraChem Server"""
        with httpx.Client() as client:
            req = client.delete(
                f"http://{self.host}:{self.frontend_port}/{path_or_filename}"
            )
        req.raise_for_status()

    def compute(
        self,
        inp_data: ProgramInput,
        raise_exc: bool = True,
        collect_stdout: bool = True,
        collect_files: bool = True,
        rm_scratch_dir: bool = True,
        **kwargs,
    ) -> ProgramOutput:
        """Top level method for performing computations with qcio inputs/outputs


        NOTE: Configuration parameters for controlling TCFrontEndClient behavior are
            found in ProgramInput.extras['tcfe:keywords'] and include:
                1. 'c0' | 'ca0 and cb0': Binary files to use as an initial guess
                    wavefunction
                2. 'scratch_messy': bool If True client will not delete files on server
                    after a computation
                3. 'uploads_messy': bool If True client will not delete uploaded c0
                    file(s) after a computation
                4. 'native_files': list[str] of filenames that will be downloaded after
                    a computation

        Args:
            prog_input: ProgramInput object
            collect_stdout: bool, if True, will collect tc.out and place in ProgramOutput
            collect_files: bool, if True, will collect all files in the scratch directory.
            rm_scratch_dir: bool, if True, will remove the scratch directory after computation
            raise_exc: bool, if True, will raise an error if the computation fails
        """

        # Do pre-compute work
        inp_data = self._pre_compute_tasks(inp_data)
        # Send calculation to TC-PBS
        try:
            prog_output = super().compute(inp_data)
        except ServerError as e:
            exc = e
            assert isinstance(e.program_output, ProgramOutput)  # type check
            prog_output = e.program_output

        # Do post-compute work
        prog_output = self._post_compute_tasks(
            prog_output,
            collect_stdout=collect_stdout,
            collect_files=collect_files,
            rm_scratch_dir=rm_scratch_dir,
        )
        if raise_exc and prog_output.success is False:
            # Append updated program_output with stdout/files to exception
            exc.program_output = prog_output
            raise exc

        return prog_output

    def _pre_compute_tasks(self, inp_data: ProgramInput) -> ProgramInput:
        """Upload wavefunction files and modify the keywords for TeraChem."""

        pi_dict = inp_data.model_dump()

        # Upload file data if provided
        if inp_data.files:
            if "c0" in inp_data.files:
                assert isinstance(inp_data.files["c0"], bytes)
                path = self.put("c0", inp_data.files["c0"])

            elif "ca0" in inp_data.files and "cb0" in inp_data.files:
                assert isinstance(inp_data.files["ca0"], bytes)
                assert isinstance(inp_data.files["cb0"], bytes)
                ca0_path = self.put("ca0", inp_data.files["ca0"])
                cb0_path = self.put("cb0", inp_data.files["cb0"])
                path = f"{ca0_path} {cb0_path}"  # TC wants two, space separated paths

            else:
                raise ValueError("Provided files not recognized by TCFrontEndClient")

            pi_dict["keywords"]["guess"] = path

        return ProgramInput(**pi_dict)

    def _post_compute_tasks(
        self,
        prog_output: ProgramOutput,
        collect_stdout: bool = True,
        collect_files: bool = True,
        rm_scratch_dir: bool = True,
    ) -> ProgramOutput:
        """Tasks to be performed after receiving a result from Terachem PBS"""

        # Collect files
        if collect_files:
            self._collect_files(prog_output)

        po_dict = prog_output.model_dump()

        # Add stdout
        if collect_stdout or prog_output.success is False:
            try:
                stdout = self.get(
                    f"{prog_output.provenance.scratch_dir}/tc.out"
                ).decode()
            except httpx.HTTPStatusError:
                stdout = "stdout could not be collected."

            po_dict["stdout"] = stdout

        # Delete uploads if not requested to keep
        if (
            self.uploads_prefix in prog_output.input_data.keywords.get("guess", "")
            and rm_scratch_dir
        ):
            for path in prog_output.input_data.keywords["guess"].split():
                self._try_delete(path)

        # Delete scratch directory
        if rm_scratch_dir:
            self._try_delete(f"{prog_output.provenance.scratch_dir}/")

        return prog_output.__class__(**po_dict)

    def _collect_files(self, prog_output: ProgramOutput) -> None:
        """Collects requested native_files.

        Parameters:
            prog_output: ProgramOutput object

        Returns:
            None: Modified result dictionary in place
        """

        scr_dir = prog_output.provenance.scratch_dir

        if scr_dir:  # may be None if the job failed
            scr_dir = str(scr_dir)
            filenames = [
                file_desc["name"]
                for file_desc in self.ls(scr_dir)
                if file_desc["type"] == "file"
            ]

            filenames.extend(
                [
                    f"scr/{file_desc['name']}"
                    for file_desc in self.ls(f"{scr_dir}/scr")
                    if file_desc["type"] == "file"
                ]
            )

            for filename in filenames:
                data: Union[str, bytes]
                try:
                    b_data: bytes = self.get(f"{scr_dir}/{filename}")
                except httpx.HTTPStatusError:
                    b_data = f"Could not find file: {filename}".encode()
                try:
                    data = b_data.decode()
                except UnicodeDecodeError:
                    # File is binary
                    data = b_data

                prog_output.results.files[filename] = data
