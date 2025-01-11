# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 23:00:57 2024

@author: User
"""

import numpy as np
from quri_parts.circuit import QuantumCircuit
from quri_parts.qulacs.sampler import create_qulacs_vector_sampler
from quri_parts.circuit.utils.circuit_drawer import draw_circuit
from CnX_gate import CnX

def binary_val(circuit, total_bits):
    sampler = create_qulacs_vector_sampler()
    sampling_result = sampler(circuit, shots=100)
    # Process each key-value pair
    for key, value in sampling_result.items():
        # Convert the key to a binary string with the specified total_bits
        binary_key = format(key, f'0{total_bits}b')
        return binary_key[::-1]

def increment_gate_with_coin(circuit, position_qbits: list, coin_qbit:int):
    tatol_qbits = position_qbits+[coin_qbit]
    for i in range(len(position_qbits)-2):
        CnX(circuit, tatol_qbits[i+1:], position_qbits[i])
    
    circuit.add_TOFFOLI_gate(coin_qbit, position_qbits[-1], position_qbits[-2])

    # Apply CNOT for qubit 0 and qubit 1
    circuit.add_CNOT_gate(coin_qbit, position_qbits[-1])

def decrement_gate_with_coin(circuit, position_qbits: list, coin_qbit:int):
    tatol_qbits = position_qbits+[coin_qbit]
    for i in range(len(position_qbits)-2):
        CnX(circuit, position_qbits[i+1:], position_qbits[i], empty=True)
    
    for i in tatol_qbits[-2:]:
        circuit.add_X_gate(i)
    
    circuit.add_TOFFOLI_gate(coin_qbit, position_qbits[-1], position_qbits[-2])

    # Apply CNOT for qubit 0 and qubit 1
    circuit.add_CNOT_gate(coin_qbit, position_qbits[-1])

    for i in tatol_qbits[-2:]:
        circuit.add_X_gate(i)
    
    
if __name__ == '__main__':
    circuit = QuantumCircuit(10)
    max_position = 3
    ancilla = max_position-1
    circuit.add_X_gate(9)
    # for i in range(5, 10):
    #     circuit.add_X_gate(i)
    # Without any operation besides initialization
    print('Without operation: ', binary_val(circuit, 10))
    
    position_qbits = [ancilla+i for i in range(max_position)]
    print(position_qbits)
    
    decrement_gate_with_coin(circuit, position_qbits, max(position_qbits)+1)
    
    # After increment
    print('After increment: ', binary_val(circuit, 10))
    
    draw_circuit(circuit)
    
    