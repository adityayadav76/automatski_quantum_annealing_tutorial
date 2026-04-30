"""
Step 6: Line-up Constraints
Enforcing ordering and sequential constraints
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def strict_ordering():
    """Enforce strict ordering: x >= y >= z"""
    
    print("=" * 60)
    print("Step 6: Line-up Constraints")
    print("=" * 60)
    
    print("\n1. Strict Ordering Constraint (x >= y >= z)")
    print("-" * 40)
    
    print("We want x >= y >= z with x, y, z in {0, 1}")
    print("Valid combinations: 000, 001, 011, 111")
    
    linear = {'x': 0, 'y': 0, 'z': 0}
    quadratic = {}
    offset = 0
    
    penalty = 10
    
    quadratic[('x', 'y')] = penalty
    quadratic[('y', 'z')] = penalty
    quadratic[('x', 'z')] = -2 * penalty
    
    linear['x'] = -penalty
    linear['y'] = 2 * penalty
    linear['z'] = -penalty
    offset = penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    x = best_state.get('x', 0)
    y = best_state.get('y', 0)
    z = best_state.get('z', 0)
    valid = x >= y >= z
    print(f"Valid ordering: {valid}")
    
    return best_state, best_cost


def monotone_sequence():
    """Monotone sequence with all valid states"""
    
    print("\n2. Monotone Sequence (0 -> 1 transition at most once)")
    print("-" * 40)
    
    print("Valid: 000, 100, 110, 111")
    print("Invalid: 001, 010, 011, 101")
    
    variables = ['a', 'b', 'c', 'd']
    linear = {v: 0 for v in variables}
    quadratic = {}
    offset = 0
    
    penalty = 10
    
    for i in range(len(variables) - 1):
        for j in range(i + 1, len(variables)):
            quadratic[(variables[i], variables[j])] = penalty
    
    for i in range(len(variables)):
        linear[variables[i]] = -penalty * (len(variables) - 1 - i)
    
    offset = penalty * len(variables) * (len(variables) - 1) // 2
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    values = [best_state.get(v, 0) for v in variables]
    print(f"Values: {values}")
    
    valid = all(values[i] <= values[i+1] for i in range(len(values)-1))
    print(f"Valid monotone: {valid}")
    
    return best_state, best_cost


def exactly_one_peak():
    """Exactly one peak in sequence"""
    
    print("\n3. Exactly One Peak (up then down)")
    print("-" * 40)
    
    variables = ['a', 'b', 'c', 'd', 'e']
    linear = {}
    quadratic = {}
    offset = 0
    
    penalty = 10
    
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            quadratic[(variables[i], variables[j])] = penalty
    
    for i in range(len(variables)):
        linear[variables[i]] = -2 * penalty * i + penalty * (len(variables) - 1)
    
    offset = penalty * (len(variables) - 1) * len(variables) // 2
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    values = [best_state.get(v, 0) for v in variables]
    print(f"Values: {values}")
    
    peaks = sum(1 for i in range(1, len(values)-1) if values[i-1] < values[i] > values[i+1])
    print(f"Number of peaks: {peaks}")
    
    return best_state, best_cost


def find_maximum():
    """Find maximum value with ordering constraint"""
    
    print("\n4. Find Maximum with Constraint")
    print("-" * 40)
    
    print("Maximize value subject to x + y + z <= 2")
    
    linear = {'x': -10, 'y': -20, 'z': -30}
    quadratic = {}
    offset = 0
    
    penalty = 20
    
    quadratic[('x', 'y')] = penalty
    quadratic[('x', 'z')] = penalty
    quadratic[('y', 'z')] = penalty
    
    linear['x'] += penalty
    linear['y'] += 2 * penalty
    linear['z'] += 3 * penalty
    offset = penalty * 3
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    print(f"Original objective value: {-best_cost}")
    print(f"Constraint satisfied: {sum(best_state.values()) <= 2}")
    
    return best_state, best_cost


if __name__ == "__main__":
    strict_ordering()
    monotone_sequence()
    exactly_one_peak()
    find_maximum()