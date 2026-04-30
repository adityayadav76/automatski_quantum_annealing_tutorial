"""
Step 7: One-Hot Encoding
Enforcing exactly-one selection constraints
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def create_one_hot_constraint(variables, penalty=10.0):
    """Create penalty terms for one-hot constraint"""
    
    linear = {v: -2 * penalty for v in variables}
    quadratic = {}
    offset = penalty
    
    for i, var_i in enumerate(variables):
        for j, var_j in enumerate(variables):
            if i < j:
                quadratic[(var_i, var_j)] = 2 * penalty
    
    return linear, quadratic, offset


def basic_one_hot():
    """Basic one-hot: exactly one of x, y, z is 1"""
    
    print("=" * 60)
    print("Step 7: One-Hot Encoding")
    print("=" * 60)
    
    print("\n1. Basic One-Hot (exactly one of x, y, z)")
    print("-" * 40)
    
    variables = ['x', 'y', 'z']
    penalty = 10
    
    linear, quadratic, offset = create_one_hot_constraint(variables, penalty)
    
    linear['x'] += 1
    linear['y'] += 2
    linear['z'] += 3
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    print("Valid solutions: (1,0,0), (0,1,0), (0,0,1)")
    print("Invalid: (0,0,0), (1,1,0), etc.")
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    selected = [k for k, v in best_state.items() if v == 1]
    print(f"Selected: {selected}")
    print(f"One-hot satisfied: {len(selected) == 1}")
    
    return best_state, best_cost


def multi_choice():
    """Multiple independent one-hot constraints"""
    
    print("\n2. Multiple One-Hot Constraints")
    print("-" * 40)
    
    print("Select one from {a,b,c} and one from {d,e,f}")
    
    group1 = ['a', 'b', 'c']
    group2 = ['d', 'e', 'f']
    penalty = 10
    
    l1, q1, o1 = create_one_hot_constraint(group1, penalty)
    l2, q2, o2 = create_one_hot_constraint(group2, penalty)
    
    l1['a'], l1['b'], l1['c'] = 5, 3, 1
    l2['d'], l2['e'], l2['f'] = 6, 4, 2
    
    linear = {**l1, **l2}
    quadratic = {**q1, **q2}
    offset = o1 + o2
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    selected1 = [k for k in group1 if best_state.get(k, 0) == 1]
    selected2 = [k for k in group2 if best_state.get(k, 0) == 1]
    print(f"Group 1 selection: {selected1}")
    print(f"Group 2 selection: {selected2}")
    
    return best_state, best_cost


def one_hot_with_weights():
    """One-hot with weighted selection"""
    
    print("\n3. One-Hot with Weighted Optimization")
    print("-" * 40)
    
    print("Choose exactly one item with maximum value")
    
    items = ['item1', 'item2', 'item3', 'item4']
    values = [10, 25, 15, 30]
    
    penalty = 20
    
    linear, quadratic, offset = create_one_hot_constraint(items, penalty)
    
    for item, value in zip(items, values):
        linear[item] += value
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    selected = [k for k, v in best_state.items() if v == 1]
    print(f"Selected item: {selected}")
    print(f"Value obtained: {values[items.index(selected[0])] if selected else 'none'}")
    
    return best_state, best_cost


def n_hot_constraint():
    """N-hot: exactly n variables are 1"""
    
    print("\n4. N-Hot Constraint (exactly 2 out of 4)")
    print("-" * 40)
    
    variables = ['a', 'b', 'c', 'd']
    n = 2
    penalty = 10
    
    linear = {v: 0 for v in variables}
    quadratic = {}
    offset = 0
    
    for i, var_i in enumerate(variables):
        for j, var_j in enumerate(variables):
            if i < j:
                quadratic[(var_i, var_j)] = 2 * penalty
    
    for var in variables:
        linear[var] = -2 * penalty * n
    
    offset = penalty * n * n
    
    linear['a'] += 1
    linear['b'] += 2
    linear['c'] += 3
    linear['d'] += 4
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    count = sum(best_state.values())
    selected = [k for k, v in best_state.items() if v == 1]
    print(f"Selected: {selected} (count: {count})")
    print(f"N-hot satisfied: {count == n}")
    
    return best_state, best_cost


def conditional_one_hot():
    """One-hot with conditional constraints"""
    
    print("\n5. Conditional One-Hot")
    print("-" * 40)
    
    print("If x=1, select exactly one of {a,b,c}")
    print("If x=0, select none of {a,b,c}")
    
    x_var = 'x'
    group = ['a', 'b', 'c']
    penalty = 10
    
    linear = {x_var: 0}
    quadratic = {}
    offset = 0
    
    for i, var_i in enumerate(group):
        linear[var_i] = 0
        
    for i, var_i in enumerate(group):
        for j, var_j in enumerate(group):
            if i < j:
                quadratic[(var_i, var_j)] = penalty * 2
    
    for var in group:
        linear[var] = -2 * penalty + penalty
        quadratic[(x_var, var)] = -2 * penalty
    
    offset = penalty
    
    linear[x_var] = 0
    linear['a'] += 1
    linear['b'] += 2
    linear['c'] += 3
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    x_val = best_state.get(x_var, 0)
    group_selected = [k for k in group if best_state.get(k, 0) == 1]
    
    print(f"x = {x_val}")
    print(f"Selected from group: {group_selected}")
    print(f"Conditional satisfied: {len(group_selected) == x_val}")
    
    return best_state, best_cost


if __name__ == "__main__":
    basic_one_hot()
    multi_choice()
    one_hot_with_weights()
    n_hot_constraint()
    conditional_one_hot()