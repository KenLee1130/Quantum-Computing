# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 16:09:55 2025

@author: User
"""
from quri_parts.circuit import QuantumCircuit
from quri_parts.qulacs.sampler import create_qulacs_vector_sampler
import numpy as np
from control_unitary_gate_matrix import controlled_unitary
from DTQW_controlled_by_msg import DTQW

def binary_val(circuit, total_bits, shots=100, **kwargs):
    sampler = create_qulacs_vector_sampler()
    sampling_result = sampler(circuit, shots=shots)
    results = {}

    # Process each key-value pair from the sampler
    for key, value in sampling_result.items():
        # Convert the key to a binary string, and reverse it
        binary_key = format(key, f'0{total_bits}b')[::-1]
        qbit_register = {}

        # Iterate over kwargs properly
        for k_key, k_val in kwargs.items():
            registr = ''
            for i in k_val:
                registr += binary_key[i]
            qbit_register[k_key] = registr
        
        # Store the results based on kwargs
        if not kwargs:
            results[binary_key] = value
        else:
            results[str(qbit_register)] = value

    return results

def Hadamard_test(circuit, target_qubits:list, control_qubits:list):
    from scipy.stats import unitary_group
    for i in control_qubits:
        circuit.add_H_gate(i)
    np.random.seed(42)
    for control in control_qubits:
        controlled_unitary(circuit, [control], target_qubits, unitary_group.rvs(2**(len(target_qubits))))
    for i in control_qubits:
        circuit.add_H_gate(i)
        
# Split input message into pairs
def split_message_into_pairs(message):
    msg_idx = {'00':0, '01':1, '10':2, '11':3}
    if len(message) % 2 != 0:
        message += '0'
    bit_pairs = [message[i:i+2] for i in range(0, len(message), 2)]
    return [[int(pair[0]), int(pair[1])] for pair in bit_pairs]

def FQHF(qubit_registr, input_message):
    circuit = QuantumCircuit(max(ancilla_qubits)+1)
    for msg in split_message_into_pairs(input_message):
        DTQW(circuit, qubit_registr['position'], qubit_registr['coin'][0], qubit_registr['msg'], walker_steps=20)
        
    Hadamard_test(circuit, qubit_registr['position'], qubit_registr['ancilla'])
    
    sampler = create_qulacs_vector_sampler()
    sampling_result = sampler(circuit, shots=int(1e+8))
    
    return sampling_result

def obtain_hash_val(measurement, total_bits):
    from collections import Counter
    results = Counter()
    # Process each key-value pair from the sampler
    for key, value in measurement.items():
        # Convert the key to a binary string, and reverse it
        binary_key = format(key, f'0{total_bits}b')[::-1][-5:]
        results[binary_key] += value
    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    
    hash_value = ''.join([binary_key for binary_key, _ in sorted_results])
    hex_string = ''.join([hex(int(hash_value[i:i+4], 2))[2:] for i in range(0, len(hash_value), 4)])

    return hex_string


if __name__ == '__main__':
    num_p_entry=5
    num_p_a_entry=num_p_entry-1
    position_qubits = [i+num_p_a_entry+1 for i in range(num_p_entry)]
    coin_qubit = max(position_qubits)+1
    msg_qubits = [coin_qubit+i for i in range(1, 3)]
    ancilla_qubits = [max(msg_qubits)+i for i in range(1, 6)]
    
    qubit_registr = {'position':[i for i in position_qubits], 'coin':[coin_qubit], 'msg':msg_qubits, 'ancilla': ancilla_qubits}
    
    input_message = '01100010110101001'
    measurement = FQHF(qubit_registr, input_message)
    
    hash_value=obtain_hash_val(measurement, max(ancilla_qubits)+1)
    print(hash_value)