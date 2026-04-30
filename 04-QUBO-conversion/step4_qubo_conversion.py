"""
Step 4: QUBO Conversion
Converting BQM to QUBO format and understanding the conversion
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def basic_qubo_conversion():
    """Basic QUBO conversion from BQM"""
    
    print("=" * 60)
    print("Step 4: QUBO Conversion")
    print("=" * 60)
    
    print("\n1. Basic QUBO Conversion")
    print("-" * 40)
    
    linear = {'x': 1.0, 'y': 2.0}
    quadratic = {('x', 'y'): -1.0}
    offset = 5.0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    print(f"Original BQM:")
    print(f"  Linear: {dict(bqm.linear)}")
    print(f"  Quadratic: {dict(bqm.quadratic)}")
    print(f"  Offset: {bqm.offset}")
    
    Q, bqm_offset = bqm.to_qubo()
    
    print(f"\nConverted QUBO:")
    print(f"  Q dict: {Q}")
    print(f"  BQM offset: {bqm_offset}")
    
    print("\nManual verification:")
    print("  For x=1, y=0: Q[(x,x)]*1 + Q[(y,y)]*0 + Q[(x,y)]*1*0 = 1*1 + 2*0 + (-1)*0 = 1")
    print("  For x=1, y=1: 1*1 + 2*1 + (-1)*1*1 = 1 + 2 - 1 = 2")
    
    return Q, bqm_offset


def qubo_to_matrix():
    """Convert QUBO dict to numpy matrix"""
    
    print("\n2. QUBO Dictionary to Matrix")
    print("-" * 40)
    
    import numpy as np
    
    linear = {'x': 1.0, 'y': 2.0, 'z': 0.5}
    quadratic = {('x', 'y'): -1.0, ('y', 'z'): -0.5, ('x', 'z'): 0.3}
    offset = 1.0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    variables = list(bqm.variables)
    n = len(variables)
    var_to_idx = {v: i for i, v in enumerate(variables)}
    
    Q, bqm_offset = bqm.to_qubo()
    
    Q_matrix = np.zeros((n, n))
    for (i, j), value in Q.items():
        idx_i = var_to_idx[i]
        idx_j = var_to_idx[j]
        Q_matrix[idx_i][idx_j] = value
    
    print(f"Variables order: {variables}")
    print(f"Q matrix:\n{Q_matrix}")
    
    print("\nSolving using matrix:")
    solver = AutomatskiInitiumSASolver(
        host=HOST, port=PORT, max_iter=1000, temp=10.0, 
        cooling_rate=0.01, num_reads=10
    )
    best_state, best_cost = solver.solve(Q)
    best_cost = best_cost + bqm_offset
    
    print(f"Best state: {best_state}")
    print(f"Best cost: {best_cost}")
    
    return Q_matrix, variables


def spin_to_qubo():
    """Convert SPIN vartype to QUBO"""
    
    print("\n3. SPIN to QUBO Conversion")
    print("-" * 40)
    
    linear = {'s1': 0.5, 's2': -0.3}
    quadratic = {('s1', 's2'): 1.0}
    offset = 2.0
    
    bqm_spin = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.SPIN)
    
    print("Original SPIN BQM:")
    print(f"  Linear: {dict(bqm_spin.linear)}")
    print(f"  Quadratic: {dict(bqm_spin.quadratic)}")
    
    bqm_binary = bqm_spin.binary
    print("\nConverted to BINARY (QUBO):")
    print(f"  Linear: {dict(bqm_binary.linear)}")
    print(f"  Quadratic: {dict(bqm_binary.quadratic)}")
    print(f"  Offset: {bqm_binary.offset}")
    
    Q, offset = bqm_binary.to_qubo()
    print(f"\nFinal QUBO Q: {Q}")
    print(f"Final offset: {offset}")
    
    return Q, offset


def ising_to_qubo():
    """Convert Ising model to QUBO"""
    
    print("\n4. Ising to QUBO Conversion")
    print("-" * 40)
    
    h = {'h1': 1.0, 'h2': 0.5}
    J = {('h1', 'h2'): -1.5}
    
    bqm_ising = dimod.BinaryQuadraticModel.from_ising(h, J)
    
    print("Original Ising:")
    print(f"  h: {h}")
    print(f"  J: {J}")
    
    Q, offset = bqm_ising.to_qubo()
    print("\nConverted QUBO:")
    print(f"  Q: {Q}")
    print(f"  Offset: {offset}")
    
    return Q, offset


def solve_converted_qubo():
    """Solve a converted QUBO problem"""
    
    print("\n5. Solving Converted QUBO")
    print("-" * 40)
    
    linear = {'a': 3, 'b': 2, 'c': 1}
    quadratic = {('a', 'b'): -2, ('b', 'c'): -1, ('a', 'c'): -1}
    offset = 0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    Q, bqm_offset = bqm.to_qubo()
    
    solver = AutomatskiInitiumSASolver(
        host=HOST, port=PORT, max_iter=1000, temp=10.0, 
        cooling_rate=0.01, num_reads=10
    )
    
    print("Sending QUBO to solver...")
    best_state, best_cost = solver.solve(Q)
    best_cost = best_cost + bqm_offset
    
    print(f"\nSolution found:")
    print(f"  Variables: {best_state}")
    print(f"  Total energy: {best_cost}")
    
    return best_state, best_cost


if __name__ == "__main__":
    basic_qubo_conversion()
    qubo_to_matrix()
    spin_to_qubo()
    ising_to_qubo()
    solve_converted_qubo()