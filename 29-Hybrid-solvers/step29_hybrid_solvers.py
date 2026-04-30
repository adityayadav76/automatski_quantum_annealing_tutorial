"""
Step 29: Hybrid Solvers
Combining classical and quantum approaches
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod
import random

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def classical_preprocessing(bqm):
    """Classical preprocessing to reduce problem size"""
    
    print("Classical preprocessing...")
    
    linear = dict(bqm.linear)
    quadratic = dict(bqm.quadratic)
    
    fixed_vars = {}
    for var, bias in linear.items():
        if abs(bias) > 100:
            fixed_vars[var] = 1 if bias > 0 else 0
    
    print(f"  Fixed variables: {fixed_vars}")
    
    return fixed_vars


def classical_postprocessing(solution, bqm):
    """Classical postprocessing to improve solution"""
    
    print("Classical postprocessing...")
    
    improved = dict(solution)
    
    for var in bqm.linear:
        if var not in improved:
            improved[var] = random.choice([0, 1])
    
    current_energy = bqm.energy(improved)
    
    for _ in range(10):
        for var in improved:
            improved[var] = 1 - improved[var]
            new_energy = bqm.energy(improved)
            if new_energy < current_energy:
                current_energy = new_energy
            else:
                improved[var] = 1 - improved[var]
    
    print(f"  Improved energy: {current_energy}")
    
    return improved


def hybrid_solve(linear, quadratic, offset):
    """Hybrid classical-quantum solve"""
    
    print("=" * 60)
    print("Step 29: Hybrid Solvers")
    print("=" * 60)
    
    print("\n1. Creating BQM")
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    print(f"  Variables: {len(bqm.variables)}")
    
    print("\n2. Classical Preprocessing")
    fixed = classical_preprocessing(bqm)
    
    reduced_linear = {k: v for k, v in bqm.linear.items() if k not in fixed}
    reduced_quadratic = {k: v for k, v in bqm.quadratic.items() 
                         if k[0] not in fixed and k[1] not in fixed}
    
    reduced_bqm = dimod.BinaryQuadraticModel(reduced_linear, reduced_quadratic, 
                                               bqm.offset, vartype=dimod.BINARY)
    print(f"  Reduced variables: {len(reduced_bqm.variables)}")
    
    print("\n3. Quantum Annealing")
    solver = AutomatskiInitiumSASolver(
        host=HOST, port=PORT, max_iter=1000, temp=10.0, 
        cooling_rate=0.01, num_reads=10
    )
    
    qubo, offset_val = reduced_bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"  Solution: {best_state}")
    print(f"  Energy: {best_cost}")
    
    print("\n4. Classical Postprocessing")
    full_solution = {**fixed, **best_state}
    improved_solution = classical_postprocessing(full_solution, bqm)
    
    final_energy = bqm.energy(improved_solution)
    print(f"  Final energy: {final_energy}")
    
    return full_solution, final_energy, improved_solution


def simple_hybrid():
    """Simple hybrid example"""
    
    print("\n1. Simple Hybrid Solver")
    print("-" * 40)
    
    linear = {'a': 5, 'b': 3, 'c': 7, 'd': 2}
    quadratic = {('a', 'b'): -2, ('c', 'd'): -3, ('a', 'c'): -1}
    offset = 0
    
    return hybrid_solve(linear, quadratic, offset)


def complex_hybrid():
    """Complex hybrid example"""
    
    print("\n2. Complex Hybrid Solver")
    print("-" * 40)
    
    linear = {'x1': 10, 'x2': 8, 'x3': 12, 'x4': 6, 'x5': 9}
    quadratic = {
        ('x1', 'x2'): -3, ('x2', 'x3'): -2, ('x3', 'x4'): -4,
        ('x4', 'x5'): -1, ('x1', 'x5'): -2, ('x1', 'x3'): -1
    }
    offset = 0
    
    return hybrid_solve(linear, quadratic, offset)


if __name__ == "__main__":
    simple_hybrid()
    complex_hybrid()