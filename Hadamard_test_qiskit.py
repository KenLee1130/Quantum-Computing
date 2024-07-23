# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:18:19 2024

@author: User
"""
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
from qiskit.extensions import UnitaryGate

def unitary_mtx(angle):
    unitary_matrix = np.array([[np.cos(angle), -np.sin(angle)], 
                                [np.sin(angle), np.cos(angle)]])
    
    return unitary_matrix

def Hadamard_test(angle):
    # Define the circuit
    circuit = QuantumCircuit(2, 1)
    
    # Apply Hadamard gate to the second qubit (|ψ>)
    circuit.h(1)

    # Apply Hadamard gate to the first qubit
    circuit.h(0)

    # Apply the controlled custom gate
    # Create a custom gate
    custom_gate = UnitaryGate(unitary_mtx(angle), label='U')
    # Create the controlled version of the custom gate
    controlled_custom_gate = custom_gate.control()
    circuit.append(controlled_custom_gate, [0, 1])

    # Apply Hadamard gate to the first qubit again
    circuit.h(0)
    
    # Measure the first qubit
    circuit.measure(0, 0)
    
    return circuit

def run_circuit(angle, draw_qc=True):
    circuit = Hadamard_test(angle)
    
    # Draw the circuit
    circuit.draw(output='mpl') if draw_qc == True else []
    
    # Run the simulation
    simulator = Aer.get_backend('qasm_simulator')
    # compiled_circuit = transpile(circuit, simulator)
    # qobj = assemble(compiled_circuit)
    result = execute(circuit, simulator, shots=1000).result()
    counts = result.get_counts(circuit)
    
    # Plot the histogram
    plot_histogram(counts)
    return {"Measurement results:": counts} 
    
if __name__ == '__main__':
    run_circuit(np.pi/2)
