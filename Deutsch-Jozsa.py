from quri_parts.circuit import QuantumCircuit, NonParametricQuantumCircuit
from quri_parts.qulacs.sampler import create_qulacs_vector_sampler
from quri_parts.circuit.utils.circuit_drawer import draw_circuit


# Define the Deutsch-Jozsa Oracle
def oracle(circuit: NonParametricQuantumCircuit, n: int, is_balanced: bool):
    if is_balanced:
        for qubit in range(n):
            circuit.add_CNOT_gate(qubit, n)
    else:
        # Constant function (no operation needed for the oracle)
        pass
    
def dj_algo(num_qubits, is_balanced:bool):
    # Create a Quantum Circuit (All qubits are |0>)
    circuit = QuantumCircuit(num_qubits+1)
    
    circuit.add_X_gate(num_qubits)
    circuit.add_H_gate(num_qubits)
    
    # DJ algo processure
    for qubit in range(num_qubits):
        circuit.add_H_gate(qubit)
        
    oracle(circuit, num_qubits, is_balanced)
    
    for qubit in range(num_qubits):
        circuit.add_H_gate(qubit)
    
    return circuit

if __name__ == '__main__':
    from collections import Counter
    # Parameters
    num_qubits=4
    is_balanced=True
    circuit = dj_algo(num_qubits, is_balanced)
    
    # Visualization of circuit
    draw_circuit(circuit)
    
    # Create and execute sampler
    sampler = create_qulacs_vector_sampler()
    sampling_result = sampler(circuit, shots=1000)
    fnc_arg_cnt = Counter()
    
    for qubit, cnt in sampling_result.items():
        fnc_arg_cnt += Counter({qubit & 2**num_qubits-1: cnt})
    print(fnc_arg_cnt)
    
