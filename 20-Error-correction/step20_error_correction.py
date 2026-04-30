"""
Step 20: Error Correction (QUBO)
Solving error correction with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def hamming_code_qubo(received):
    """
    QUBO for Hamming code error correction
    
    received: list of received bits
    """
    
    n = len(received)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    syndrome_penalty = 100
    
    parity_positions = [1, 2, 4, 8]
    data_positions = [i for i in range(n) if i + 1 not in parity_positions]
    
    for i in range(n):
        linear[f'e_{i}'] = 1
    
    syndrome_equations = []
    for p in parity_positions:
        syndrome_eq = []
        for i in range(n):
            if (i + 1) & p:
                syndrome_eq.append(i)
        syndrome_equations.append(syndrome_eq)
    
    for eq_idx, eq in enumerate(syndrome_equations):
        expected = 0
        for i in eq:
            expected = (expected + received[i]) % 2
        
        linear_eq = {}
        quadratic_eq = {}
        
        for i in eq:
            linear_eq[f'e_{i}'] = 1
        
        for i in range(len(eq)):
            for j in range(i + 1, len(eq)):
                quadratic_eq[(eq[i], eq[j])] = 2
        
        offset_eq = len(eq) * (len(eq) - 1) // 2 + expected
        
        for var, coeff in linear_eq.items():
            linear[var] = linear.get(var, 0) + syndrome_penalty * coeff
        
        for (i, j), coeff in quadratic_eq.items():
            key = (f'e_{i}', f'e_{j}')
            quadratic[key] = quadratic.get(key, 0) + syndrome_penalty * coeff
        
        offset += syndrome_penalty * offset_eq
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, n


def solve_error_correction(received):
    """Solve error correction"""
    
    print("=" * 60)
    print("Step 20: Error Correction (QUBO)")
    print("=" * 60)
    
    print(f"\nReceived bits: {received}")
    
    bqm, n = hamming_code_qubo(received)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    errors = [best_state.get(f'e_{i}', 0) for i in range(n)]
    print(f"Detected errors: {errors}")
    
    corrected = [(received[i] + errors[i]) % 2 for i in range(n)]
    print(f"Corrected bits: {corrected}")
    
    return best_state, best_cost, errors, corrected


def single_error():
    """Single bit error correction"""
    
    print("\n1. Single Bit Error (Hamming[7,4])")
    print("-" * 40)
    
    original = [1, 0, 1, 1, 0, 0, 1]
    received = [1, 0, 0, 1, 0, 0, 1]
    
    return solve_error_correction(received)


def no_error():
    """No error case"""
    
    print("\n2. No Error")
    print("-" * 40)
    
    received = [1, 0, 1, 1, 0, 0, 1]
    
    return solve_error_correction(received)


def different_error():
    """Different single error"""
    
    print("\n3. Different Single Error")
    print("-" * 40)
    
    received = [1, 0, 1, 0, 0, 0, 1]
    
    return solve_error_correction(received)


def extended_hamming():
    """Extended Hamming code"""
    
    print("\n4. Extended Hamming (simulated)")
    print("-" * 40)
    
    received = [1, 1, 0, 1, 0, 1, 0, 1]
    
    return solve_error_correction(received[:7])


if __name__ == "__main__":
    single_error()
    no_error()
    different_error()
    extended_hamming()