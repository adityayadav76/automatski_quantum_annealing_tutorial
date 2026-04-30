"""
Step 8: Knapsack Problem
Classic 0-1 knapsack problem solved with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def knapsack_qubo(items, capacity):
    """
    Create QUBO for knapsack problem
    
    items: list of (weight, value) tuples
    capacity: maximum weight allowed
    """
    
    penalty = sum(item[1] for item in items) * 2
    
    linear = {}
    quadratic = {}
    offset = 0
    
    for i, (weight, value) in enumerate(items):
        var = f'item_{i}'
        linear[var] = -value
        
        quadratic[(var, var)] = penalty * weight * weight
    
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            var_i = f'item_{i}'
            var_j = f'item_{j}'
            weight_i, _ = items[i]
            weight_j, _ = items[j]
            quadratic[(var_i, var_j)] = 2 * penalty * weight_i * weight_j
    
    for weight, _ in items:
        offset += penalty * weight * capacity
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, penalty


def solve_knapsack(items, capacity):
    """Solve knapsack problem"""
    
    print("=" * 60)
    print("Step 8: Knapsack Problem")
    print("=" * 60)
    
    print(f"\nItems (weight, value): {items}")
    print(f"Capacity: {capacity}")
    
    bqm, penalty = knapsack_qubo(items, capacity)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    total_weight = 0
    total_value = 0
    selected = []
    
    for i, (weight, value) in enumerate(items):
        var = f'item_{i}'
        if best_state.get(var, 0) == 1:
            total_weight += weight
            total_value += value
            selected.append(i)
    
    print(f"Selected items: {selected}")
    print(f"Total weight: {total_weight} (capacity: {capacity})")
    print(f"Total value: {total_value}")
    print(f"Feasible: {total_weight <= capacity}")
    
    return best_state, best_cost, selected, total_value


def small_knapsack():
    """Small example with known optimal"""
    
    print("\n1. Small Knapsack (4 items)")
    print("-" * 40)
    
    items = [
        (2, 10),
        (3, 15),
        (5, 40),
        (7, 50)
    ]
    capacity = 10
    
    return solve_knapsack(items, capacity)


def medium_knapsack():
    """Medium example"""
    
    print("\n2. Medium Knapsack (6 items)")
    print("-" * 40)
    
    items = [
        (2, 6),
        (2, 10),
        (3, 12),
        (5, 16),
        (7, 20),
        (9, 25)
    ]
    capacity = 15
    
    return solve_knapsack(items, capacity)


def multi_constraint_knapsack():
    """Knapsack with multiple constraints"""
    
    print("\n3. Multi-Constraint Knapsack")
    print("-" * 40)
    
    print("Maximize value with two weight constraints")
    
    items = [
        (2, 3, 10),
        (3, 2, 15),
        (5, 4, 40),
        (7, 5, 50),
        (2, 1, 5),
        (4, 3, 25)
    ]
    
    capacity1 = 12
    capacity2 = 10
    
    penalty = sum(item[2] for item in items) * 2
    
    linear = {}
    quadratic = {}
    offset = 0
    
    for i, (w1, w2, value) in enumerate(items):
        var = f'item_{i}'
        linear[var] = -value
        quadratic[(var, var)] = penalty * (w1**2 + w2**2)
    
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            var_i = f'item_{i}'
            var_j = f'item_{j}'
            w1_i, w2_i, _ = items[i]
            w1_j, w2_j, _ = items[j]
            quadratic[(var_i, var_j)] = 2 * penalty * (w1_i * w1_j + w2_i * w2_j)
    
    for w1, w2, _ in items:
        offset += penalty * (w1 * capacity1 + w2 * capacity2)
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    total_w1 = sum(items[i][0] for i in range(len(items)) if best_state.get(f'item_{i}', 0) == 1)
    total_w2 = sum(items[i][1] for i in range(len(items)) if best_state.get(f'item_{i}', 0) == 1)
    total_value = sum(items[i][2] for i in range(len(items)) if best_state.get(f'item_{i}', 0) == 1)
    
    print(f"Solution: {best_state}")
    print(f"Weight1: {total_w1}/{capacity1}, Weight2: {total_w2}/{capacity2}")
    print(f"Total value: {total_value}")
    
    return best_state, best_cost


def bounded_knapsack():
    """Bounded knapsack with item limits"""
    
    print("\n4. Bounded Knapsack (limited copies)")
    print("-" * 40)
    
    print("Each item can be selected 0-2 times")
    
    base_items = [
        (2, 10),
        (3, 15),
        (5, 25)
    ]
    capacity = 12
    max_copies = 2
    
    variables = []
    linear = {}
    quadratic = {}
    offset = 0
    
    penalty = sum(v for _, v in base_items) * 4
    
    for item_idx, (weight, value) in enumerate(base_items):
        for copy in range(max_copies + 1):
            var = f'item_{item_idx}_{copy}'
            variables.append(var)
            linear[var] = -value
    
    for i, var_i in enumerate(variables):
        for j, var_j in enumerate(variables):
            if i < j:
                weight_i = base_items[i // (max_copies + 1)][0]
                weight_j = base_items[j // (max_copies + 1)][0]
                quadratic[(var_i, var_j)] = penalty * weight_i * weight_j
    
    for var in variables:
        weight = base_items[int(var.split('_')[1])][0]
        quadratic[(var, var)] = penalty * weight * weight
    
    offset = penalty * capacity * capacity
    
    for item_idx in range(len(base_items)):
        group_vars = [v for v in variables if v.startswith(f'item_{item_idx}_')]
        for i, var_i in enumerate(group_vars):
            for j, var_j in enumerate(group_vars):
                if i < j:
                    if (var_i, var_j) in quadratic:
                        quadratic[(var_i, var_j)] += -penalty
                    else:
                        quadratic[(var_i, var_j)] = -penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    
    total_weight = sum(base_items[int(v.split('_')[1])][0] for v in variables if best_state.get(v, 0) == 1)
    total_value = sum(base_items[int(v.split('_')[1])][1] for v in variables if best_state.get(v, 0) == 1)
    
    print(f"Total weight: {total_weight}/{capacity}")
    print(f"Total value: {total_value}")
    
    return best_state, best_cost


if __name__ == "__main__":
    small_knapsack()
    medium_knapsack()
    multi_constraint_knapsack()
    bounded_knapsack()