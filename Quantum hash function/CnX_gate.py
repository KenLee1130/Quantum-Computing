# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:25:25 2024

@author: User
"""
import numpy as np
from quri_parts.circuit import QuantumCircuit
from quri_parts.qulacs.sampler import create_qulacs_vector_sampler
from quri_parts.circuit.utils.circuit_drawer import draw_circuit

def CnX(circuit, control, target, empty=False):
    num_ancilla = len(control)-1
    def black_CnX():
        circuit.add_TOFFOLI_gate(control[-1], control[-2], 0)
        for a in range(1, num_ancilla):
            circuit.add_TOFFOLI_gate(a-1, sorted(control, reverse=True)[a+1], a)
        circuit.add_CNOT_gate(num_ancilla-1, target)
        for a in range(1, num_ancilla):
            circuit.add_TOFFOLI_gate(num_ancilla-a-1, control[a-1], num_ancilla-a)
        circuit.add_TOFFOLI_gate(control[-1], control[-2], 0)
    
    if empty==False:
        return black_CnX()
    else:
        for i in control:
            circuit.add_X_gate(i)
        black_CnX()
        for i in control:
            circuit.add_X_gate(i)
        return 

if __name__ == '__main__':
    circuit = QuantumCircuit(10)
    position = [7, 8, 9]
    for i in [7, 8, 9]:
        circuit.add_X_gate(i)
    CnX(circuit, position, 6, empty=False)
    
    draw_circuit(circuit)
    
    sampler = create_qulacs_vector_sampler()
    sampling_result = sampler(circuit, shots=100)
    
    new_key = format(list(sampling_result.keys())[0], f'0{10}b')
    print(new_key)