# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 21:35:11 2024

@author: User
"""

import numpy as np
from scipy.linalg import block_diag
from quri_parts.circuit import QuantumCircuit
from quri_parts.circuit.utils.circuit_drawer import draw_circuit
from binary_vals import binary_val
from indecrement_gate_v1 import increment_gate_with_coin, decrement_gate_with_coin
        
def DTQW(circuit, position_qbits: list, coin_qbit: int, msg_qbits: list, walker_steps=1, theta_idxs=[1, 3]):
    def controlled_unitary_mtx(num_qbits, idx):
        thetas = {0:360*5/32, 1:360*3/32, 2:360*11/32, 3:360*7/32} # {0:360*1/8, 1:360*3/8, 2:360*5/8, 3:360*7/8}
        I = np.eye(2**(num_qbits)-2)
        rotation_mtx = [
            [np.cos(thetas[idx]), np.sin(thetas[idx])], 
            [np.sin(thetas[idx]), -np.cos(thetas[idx])]
            ]
        
        return block_diag(I, rotation_mtx)
    
    msg = [[0, 0], [0, 1], [1, 0], [1, 1]]
    for _ in range(walker_steps):
        for i in range(4):
            msg_qbits_assignment = msg[i]
            for j in range(len(msg_qbits)):
                if msg_qbits_assignment[j]==0:
                    circuit.add_X_gate(msg_qbits[j])
            circuit.add_UnitaryMatrix_gate([coin_qbit, msg_qbits[0], msg_qbits[1]], controlled_unitary_mtx(3, i))
            for j in range(len(msg_qbits)):
                if msg_qbits_assignment[j]==0:
                    circuit.add_X_gate(msg_qbits[j])
        increment_gate_with_coin(circuit, position_qbits, coin_qbit)
        decrement_gate_with_coin(circuit, position_qbits, coin_qbit)
    
if __name__ == '__main__':
    num_total_qbits=13
    num_p_entry=2
    num_p_a_entry=num_p_entry-1
    position_qubits = [i+num_p_a_entry+1 for i in range(num_p_entry)]
    coin_qubit = max(position_qubits)+1
    msg_qubits = [coin_qubit+i for i in range(1, 3)]
    
    print(position_qubits, coin_qubit, msg_qubits)
    qubit_registr = {'position':[i for i in position_qubits], 'coin':[coin_qubit], 'msg':msg_qubits}
    circuit = QuantumCircuit(num_total_qbits)
    # circuit.add_X_gate(msg_qubits[0])
    # circuit.add_X_gate(msg_qubits[1])
    print('Before QW: ', binary_val(circuit, num_total_qbits, **qubit_registr))
    
    DTQW(circuit, [i for i in position_qubits], coin_qubit, msg_qubits, walker_steps=1)
    
    print('After QW: ', binary_val(circuit, num_total_qbits, **qubit_registr))
    
    draw_circuit(circuit)