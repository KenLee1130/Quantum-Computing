# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:57:29 2024

@author: User
"""

import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram

# Define the Deutsch-Jozsa Oracle
def oracle(circuit, n: int, is_balanced: bool):
    if is_balanced:
        for qubit in range(n):
            circuit.cnot(qubit, n)
    else:
        # Constant function (no operation needed for the oracle)
        pass
    
def Deutsch_Jozsa(num_qubits, is_balanced=True):
    # Define the circuit
    circuit = QuantumCircuit(num_qubits+1, num_qubits)
    
    # Apply Hadamard gate to the second qubit (|ψ>)
    circuit.x(num_qubits)
    circuit.h(num_qubits)
    
    # Apply Hadamard gate to the first qubit
    for qubit in range(num_qubits):
        circuit.h(qubit)

    oracle(circuit, num_qubits, is_balanced=is_balanced)

    # Apply Hadamard gate to the first qubit again
    for qubit in range(num_qubits):
        circuit.h(qubit)
    
    # Measure the first qubit
    for qubit in range(num_qubits):
        circuit.measure(qubit, qubit)
    
    return circuit

def run_circuit(num_qubits, draw_qc=True, is_balanced=True):
    circuit = Deutsch_Jozsa(num_qubits, is_balanced)
    
    # Draw the circuit
    circuit.draw(output='mpl') if draw_qc == True else []
    
    # Run the simulation
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(circuit, simulator)
    qobj = assemble(compiled_circuit)
    result = execute(circuit, simulator, shots=1000).result()
    counts = result.get_counts(circuit)
    print(counts)
    # Plot the histogram
    plot_histogram(counts)
    return {"Measurement results:": counts} 
    
if __name__ == '__main__':
    run_circuit(4, draw_qc=True, is_balanced=False)