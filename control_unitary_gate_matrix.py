import numpy as np
from itertools import product
from quri_parts.circuit.gate import QuantumGate

def controlled_unitary(circuit, control_qubits, target_qubits, U):
    """
    Constructs the matrix representation of a controlled-unitary gate 
    with arbitrary control and target qubits.

    Parameters:
    control_qubits -- List of indices of control qubits
    target_qubits  -- List of indices of target qubits
    U              -- Unitary matrix acting on the target qubits, 
                      with dimensions 2^t x 2^t, where t is the number of target qubits

    Returns:
    The matrix representation of the controlled-unitary gate
    """
    # Total number of control and target qubits
    m = len(control_qubits) + len(target_qubits)
    
    # Dimensionality of the Hilbert space for the control and target qubits
    dim = 2 ** m

    # Initialize the controlled-unitary gate matrix as the identity matrix
    U_controlled = np.eye(dim, dtype=complex)

    # Iterate over all possible quantum states
    for i in range(dim):
        # Convert the index into a binary representation (list of bits)
        state_bits = [(i >> bit) & 1 for bit in reversed(range(m))]

        # Check if all control qubits are in state 1
        control_state = [state_bits[q] for q in range(len(control_qubits))]
        if all(control_state):
            # Extract the indices and values of the target qubits
            target_state = [state_bits[len(control_qubits) + idx] for idx in range(len(target_qubits))]

            # Compute the basis state index for the target qubits
            target_dim = len(target_qubits)
            target_index = sum([bit << (target_dim - 1 - idx) for idx, bit in enumerate(target_state)])

            # Apply the unitary operation U to the target qubits and compute new target states
            for t in range(2 ** target_dim):
                # Generate new target state bits
                new_target_bits = [(t >> (target_dim - 1 - idx)) & 1 for idx in range(target_dim)]

                # Build the new state for the entire system
                new_state_bits = state_bits.copy()
                for idx, q in enumerate(new_target_bits):
                    new_state_bits[len(control_qubits) + idx] = q

                # Compute the new index for the full system state
                j = sum([bit << (m - 1 - idx) for idx, bit in enumerate(new_state_bits)])

                # Update the controlled-unitary matrix
                U_controlled[j, i] = U[t, target_index]
        else:
            # Keep the state unchanged if control qubits are not all 1
            U_controlled[i, i] = 1.0
    
    qbits_span = target_qubits+control_qubits
    custom_gate = QuantumGate(name='UnitaryMatrix', 
                              target_indices=qbits_span, 
                              unitary_matrix=U_controlled)
    circuit.add_gate(custom_gate)

