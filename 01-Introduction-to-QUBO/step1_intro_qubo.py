"""
Step 1: Introduction to QUBO
A simple example demonstrating basic QUBO formulation and solution
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80

def simple_qubo_demo():
    """Demonstrate a simple QUBO problem: minimize x + y - xy"""
    
    print("=" * 60)
    print("Step 1: Introduction to QUBO")
    print("=" * 60)
    
    print("\nProblem: minimize f(x,y) = x + y - xy")
    print("Subject to: x, y in {0, 1}")
    
    linear = {'x': 1, 'y': 1}
    quadratic = {('x', 'y'): -1}
    offset = 0.0
    
    print("\nQUBO formulation:")
    print(f"  Linear terms: {linear}")
    print(f"  Quadratic terms: {quadratic}")
    print(f"  Offset: {offset}")
    
    print("\nEnumerating all solutions:")
    solutions = [
        ({'x': 0, 'y': 0}, 0),
        ({'x': 0, 'y': 1}, 1),
        ({'x': 1, 'y': 0}, 1),
        ({'x': 1, 'y': 1}, 1),
    ]
    for sol, energy in solutions:
        print(f"  {sol} -> Energy: {energy}")
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    print("\n" + "=" * 60)
    print("Solving using AutomatskiInitium Solver...")
    print("=" * 60)
    
    solver = AutomatskiInitiumSASolver(
        host=HOST, 
        port=PORT, 
        max_iter=1000, 
        temp=10.0, 
        cooling_rate=0.01, 
        num_reads=10
    )
    
    qubo, offset = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset
    
    print(f"\nOptimal Solution Found:")
    print(f"  Variables: {best_state}")
    print(f"  Energy: {best_cost}")
    
    expected_energy = 0
    if best_cost == expected_energy:
        print(f"\n✓ SUCCESS: Found expected minimum energy of {expected_energy}")
    else:
        print(f"\n⚠ Note: Expected minimum energy is {expected_energy}")
    
    return best_state, best_cost


def more_complex_example():
    """Another example with 3 variables"""
    
    print("\n" + "=" * 60)
    print("Bonus Example: 3-variable QUBO")
    print("=" * 60)
    
    print("\nProblem: minimize f(x,y,z) = 3x + 2y + z - 2xy - xz")
    
    linear = {'x': 3, 'y': 2, 'z': 1}
    quadratic = {('x', 'y'): -2, ('x', 'z'): -1}
    offset = 0.0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(
        host=HOST, 
        port=PORT, 
        max_iter=1000, 
        temp=10.0, 
        cooling_rate=0.01, 
        num_reads=10
    )
    
    qubo, offset = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    return best_state, best_cost


if __name__ == "__main__":
    simple_qubo_demo()
    more_complex_example()