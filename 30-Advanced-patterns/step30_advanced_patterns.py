"""
Step 30: Advanced Patterns
Advanced QUBO patterns and techniques
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def adaptive_penalty(linear, quadratic, constraint_violations):
    """Adaptive penalty based on constraint violations"""
    
    base_penalty = 10
    
    for violation in constraint_violations:
        base_penalty *= 1.5
    
    return base_penalty


def nested_qubo():
    """Nested QUBO structure"""
    
    print("=" * 60)
    print("Step 30: Advanced Patterns")
    print("=" * 60)
    
    print("\n1. Nested QUBO")
    print("-" * 40)
    
    print("  Level 1: Coarse solution")
    linear1 = {'a': 5, 'b': 3}
    quadratic1 = {('a', 'b'): -2}
    bqm1 = dimod.BinaryQuadraticModel(linear1, quadratic1, 0, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    qubo1, off1 = bqm1.to_qubo()
    state1, cost1 = solver.solve(qubo1)
    cost1 += off1
    
    print(f"    Level 1 solution: {state1}, cost: {cost1}")
    
    print("  Level 2: Fine-grained solution")
    a_val = state1.get('a', 0)
    b_val = state1.get('b', 0)
    
    linear2 = {'x1': 1, 'x2': 2, 'x3': 3}
    quadratic2 = {('x1', 'x2'): -1, ('x2', 'x3'): -1}
    bqm2 = dimod.BinaryQuadraticModel(linear2, quadratic2, 0, vartype=dimod.BINARY)
    
    qubo2, off2 = bqm2.to_qubo()
    state2, cost2 = solver.solve(qubo2)
    cost2 += off2
    
    print(f"    Level 2 solution: {state2}, cost: {cost2}")
    
    return state1, cost1, state2, cost2


def multi_objective():
    """Multi-objective optimization"""
    
    print("\n2. Multi-Objective Optimization")
    print("-" * 40)
    
    print("  Objective 1: Minimize cost")
    print("  Objective 2: Maximize quality")
    
    linear_cost = {'a': 3, 'b': 4, 'c': 2}
    quadratic_cost = {('a', 'b'): 1, ('b', 'c'): 1}
    
    linear_quality = {'a': -5, 'b': -3, 'c': -4}
    quadratic_quality = {('a', 'b'): -1, ('b', 'c'): -1}
    
    weight_cost = 0.6
    weight_quality = 0.4
    
    linear = {k: linear_cost[k] * weight_cost + linear_quality[k] * weight_quality 
              for k in linear_cost}
    quadratic = {}
    for k in quadratic_cost:
        quadratic[k] = quadratic_cost[k] * weight_cost + quadratic_quality.get(k, 0) * weight_quality
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, 0, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    qubo, offset = bqm.to_qubo()
    state, cost = solver.solve(qubo)
    cost += offset
    
    print(f"  Solution: {state}")
    print(f"  Combined cost: {cost}")
    
    return state, cost


def decomposition():
    """Problem decomposition"""
    
    print("\n3. Problem Decomposition")
    print("-" * 40)
    
    print("  Decomposing into subproblems...")
    
    sub1_vars = ['a', 'b']
    sub2_vars = ['c', 'd']
    
    sub1 = dimod.BinaryQuadraticModel({'a': 1, 'b': 2}, {('a', 'b'): -1}, 0, dimod.BINARY)
    sub2 = dimod.BinaryQuadraticModel({'c': 3, 'd': 1}, {('c', 'd'): -2}, 0, dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo1, off1 = sub1.to_qubo()
    state1, cost1 = solver.solve(qubo1)
    cost1 += off1
    
    qubo2, off2 = sub2.to_qubo()
    state2, cost2 = solver.solve(qubo2)
    cost2 += off2
    
    combined = {**state1, **state2}
    total_cost = cost1 + cost2
    
    print(f"  Subproblem 1: {state1}, cost: {cost1}")
    print(f"  Subproblem 2: {state2}, cost: {cost2}")
    print(f"  Combined solution: {combined}")
    print(f"  Total cost: {total_cost}")
    
    return combined, total_cost


def advanced_constraints():
    """Advanced constraint patterns"""
    
    print("\n4. Advanced Constraints")
    print("-" * 40)
    
    print("  Soft constraints with Lagrange multipliers")
    
    variables = ['x', 'y', 'z']
    penalty = 10
    
    linear = {'x': 1, 'y': 2, 'z': 3}
    quadratic = {}
    
    quadratic[('x', 'y')] = penalty * 2
    quadratic[('y', 'z')] = penalty * 2
    
    offset = penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    qubo, offset_val = bqm.to_qubo()
    state, cost = solver.solve(qubo)
    cost += offset_val
    
    print(f"  Solution: {state}")
    print(f"  Energy: {cost}")
    
    return state, cost


def benchmarking():
    """Benchmark different patterns"""
    
    print("\n5. Benchmarking")
    print("-" * 40)
    
    results = []
    
    for n in [5, 10, 15]:
        linear = {f'v{i}': i % 3 + 1 for i in range(n)}
        quadratic = {(f'v{i}', f'v{j}'): -1 for i in range(n) for j in range(i+1, n) if j - i < 3}
        
        bqm = dimod.BinaryQuadraticModel(linear, quadratic, 0, vartype=dimod.BINARY)
        
        solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
        qubo, offset = bqm.to_qubo()
        state, cost = solver.solve(qubo)
        cost += offset
        
        results.append((n, len(bqm.variables), cost))
        print(f"  n={n}, vars={len(bqm.variables)}, cost={cost}")
    
    return results


if __name__ == "__main__":
    nested_qubo()
    multi_objective()
    decomposition()
    advanced_constraints()
    benchmarking()