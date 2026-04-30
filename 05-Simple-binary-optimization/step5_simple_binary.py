"""
Step 5: Simple Binary Optimization
Basic binary optimization problems
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def weighted_sum_minimization():
    """Minimize weighted sum of binary variables"""
    
    print("=" * 60)
    print("Step 5: Simple Binary Optimization")
    print("=" * 60)
    
    print("\n1. Weighted Sum Minimization")
    print("-" * 40)
    
    print("Problem: minimize 3*x + 2*y + 5*z")
    
    linear = {'x': 3, 'y': 2, 'z': 5}
    quadratic = {}
    offset = 0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy (should be 0 since all weights are positive): {best_cost}")
    
    return best_state, best_cost


def maximize_with_negative_weights():
    """Maximization via negative weights (minimize -value)"""
    
    print("\n2. Maximization via Negative Weights")
    print("-" * 40)
    
    print("Problem: maximize 10*x + 15*y")
    print("Equivalently: minimize -10*x - 15*y")
    
    linear = {'x': -10, 'y': -15}
    quadratic = {}
    offset = 0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    print("To get original objective value: -energy = {-}".format(-best_cost))
    
    return best_state, best_cost


def simple_quadratic():
    """Simple quadratic objective"""
    
    print("\n3. Simple Quadratic Objective")
    print("-" * 40)
    
    print("Problem: minimize x + y + xy")
    
    linear = {'x': 1, 'y': 1}
    quadratic = {('x', 'y'): 1}
    offset = 0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    print("\nAll possible solutions:")
    for x in [0, 1]:
        for y in [0, 1]:
            energy = x + y + x*y
            print(f"  x={x}, y={y} -> energy = {energy}")
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    return best_state, best_cost


def pairwise_interactions():
    """Problem with pairwise interactions"""
    
    print("\n4. Pairwise Interactions")
    print("-" * 40)
    
    print("Problem: minimize x + y + z - xy - yz")
    
    linear = {'x': 1, 'y': 1, 'z': 1}
    quadratic = {('x', 'y'): -1, ('y', 'z'): -1}
    offset = 0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    print("All possible solutions:")
    for x in [0, 1]:
        for y in [0, 1]:
            for z in [0, 1]:
                energy = x + y + z - x*y - y*z
                print(f"  x={x}, y={y}, z={z} -> energy = {energy}")
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    return best_state, best_cost


def select_k_out_of_n():
    """Select exactly k out of n variables to be 1"""
    
    print("\n5. Select Exactly K Out of N")
    print("-" * 40)
    
    print("Problem: Select exactly 2 out of 4 variables")
    print("With bonus for selecting higher indexed ones")
    
    linear = {'a': -1, 'b': -2, 'c': -3, 'd': -4}
    quadratic = {}
    offset = 0
    
    n = 4
    k = 2
    penalty = 10
    
    for i in range(n):
        for j in range(n):
            if i < j:
                quadratic[(list(linear.keys())[i], list(linear.keys())[j])] = 2 * penalty
    
    for var in linear:
        linear[var] -= penalty * k
    
    offset += penalty * k * k
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    selected = [k for k, v in best_state.items() if v == 1]
    print(f"Solution: {best_state}")
    print(f"Selected: {selected}")
    print(f"Count: {len(selected)}")
    print(f"Energy: {best_cost}")
    
    return best_state, best_cost


if __name__ == "__main__":
    weighted_sum_minimization()
    maximize_with_negative_weights()
    simple_quadratic()
    pairwise_interactions()
    select_k_out_of_n()