from typing import Optional, Tuple

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, Gate
from qiskit.circuit.library import PhaseGate, RGate, RXGate, RYGate, HGate, RZGate, UGate, XGate, YGate, ZGate, SXGate, \
    SXdgGate, CXGate, CYGate, CZGate, CPhaseGate, SwapGate, iSwapGate

from planqk.client.model_enums import Job_Input_Format
from planqk.qiskit import PlanqkQiskitBackend
from planqk.qiskit.options import OptionsV2
from planqk.qiskit.provider import PlanqkQuantumProvider
from planqk.qiskit.providers.qryd.pcp_gate import PCPGate
from planqk.qiskit.providers.qryd.pcz_gate import PCZGate
from planqk.qiskit.providers.qryd.qryd_converter_utils import convert_to_wire_format

qryd_gate_name_mapping = {
    "p": PhaseGate(Parameter("lambda")),
    "r": RGate(Parameter("theta"), Parameter("phi")),
    "rx": RXGate(Parameter("theta")),
    "ry": RYGate(Parameter("theta")),
    "pcz": PCZGate(),
    "pcp": PCPGate(Parameter("lambda")),
    "h": HGate(),
    "rz": RZGate(Parameter("theta")),
    "u": UGate(Parameter("theta"), Parameter("phi"), Parameter("lambda")),
    "x": XGate(),
    "y": YGate(),
    "z": ZGate(),
    "sx": SXGate(),
    "sxdg": SXdgGate(),
    "cx": CXGate(),
    "cy": CYGate(),
    "cz": CZGate(),
    "cp": CPhaseGate(Parameter("theta")),
    "swap": SwapGate(),
    "iswap": iSwapGate()
}

@PlanqkQuantumProvider.register_backend("qryd.sim.square")
@PlanqkQuantumProvider.register_backend("qryd.sim.triangle")
class PlanqkQrydQiskitBackend(PlanqkQiskitBackend):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _default_options(cls):
        return OptionsV2(
            shots=1024,
            memory=False,
            seed_simulator=None,
            seed_compiler=None,
            allow_compilation=True,
            fusion_max_qubits=4,
            use_extended_set=True,
            use_reverse_traversal=True,
            extended_set_size=5,
            extended_set_weight=0.5,
            reverse_traversal_iterations=3,
        )

    def _to_gate(self, name: str) -> Optional[Gate]:
        name = name.lower()
        return qryd_gate_name_mapping.get(name, None) or Gate(name, 0, [])

    def _get_single_qubit_gate_properties(self) -> dict:
        qubits = self.backend_info.configuration.qubits
        return {(int(qubit.id),): None for qubit in qubits}

    def _get_multi_qubit_gate_properties(self) -> dict:
        # QRyd backend emulators are fully connected
        qubits = self.backend_info.configuration.qubits
        return {(int(qubit1.id), int(qubit2.id)): None for qubit1 in qubits for qubit2 in qubits
                if qubit1.id != qubit2.id}

    def _convert_to_job_input(self, job_input, options=None) -> Tuple[Job_Input_Format, dict]:
        return convert_to_wire_format(circuit=job_input, options=options)

    def _convert_to_job_params(self, job_input: QuantumCircuit = None, options=None) -> dict:
        return {
            "format": "qoqo",
            "backend": "",  # Backend is set in the middleware
            "fusion_max_qubits": options.fusion_max_qubits,
            "seed_simulator": options.seed_simulator,
            "seed_compiler": options.seed_compiler,
            "allow_compilation": options.allow_compilation,
            "pcz_theta": float(PCZGate().get_theta()),
            "use_extended_set": options.use_extended_set,
            "use_reverse_traversal": options.use_reverse_traversal,
            "extended_set_size": options.extended_set_size,
            "extended_set_weight": options.extended_set_weight,
            "reverse_traversal_iterations": options.reverse_traversal_iterations,
        }

    def _get_job_input_format(self) -> Job_Input_Format:
        return Job_Input_Format.QOQO
