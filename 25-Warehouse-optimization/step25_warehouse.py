"""
Step 25: Warehouse Optimization (QUBO)
Solving warehouse problems with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def warehouse_placement_qubo(items, locations, frequencies):
    """
    QUBO for warehouse item placement
    
    items: list of item IDs
    locations: list of location IDs
    frequencies: dict of item -> pick frequency
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 50
    distance_penalty = 10
    
    for item in items:
        for loc in locations:
            linear[(item, loc)] = -frequencies.get(item, 1)
    
    for item in items:
        for loc1 in locations:
            for loc2 in locations:
                if loc1 != loc2:
                    quadratic[((item, loc1), (item, loc2))] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    for loc in locations:
        for item1 in items:
            for item2 in items:
                if item1 != item2:
                    quadratic[((item1, loc), (item2, loc))] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, items, locations


def solve_warehouse(items, locations, frequencies):
    """Solve warehouse optimization"""
    
    print("=" * 60)
    print("Step 25: Warehouse Optimization (QUBO)")
    print("=" * 60)
    
    print(f"\nItems: {items}")
    print(f"Locations: {locations}")
    print(f"Frequencies: {frequencies}")
    
    bqm, items, locations = warehouse_placement_qubo(items, locations, frequencies)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    placement = {}
    for item in items:
        for loc in locations:
            if best_state.get((item, loc), 0) == 1:
                placement[item] = loc
    
    print(f"Placement: {placement}")
    
    return best_state, best_cost, placement


def simple_warehouse():
    """Simple warehouse"""
    
    print("\n1. Simple Warehouse Placement")
    print("-" * 40)
    
    items = ['A', 'B', 'C']
    locations = ['L1', 'L2', 'L3']
    frequencies = {'A': 10, 'B': 5, 'C': 8}
    
    return solve_warehouse(items, locations, frequencies)


def larger_warehouse():
    """Larger warehouse"""
    
    print("\n2. Larger Warehouse")
    print("-" * 40)
    
    items = ['P1', 'P2', 'P3', 'P4', 'P5']
    locations = ['A1', 'A2', 'A3', 'B1', 'B2']
    frequencies = {'P1': 20, 'P2': 15, 'P3': 10, 'P4': 8, 'P5': 5}
    
    return solve_warehouse(items, locations, frequencies)


if __name__ == "__main__":
    simple_warehouse()
    larger_warehouse()