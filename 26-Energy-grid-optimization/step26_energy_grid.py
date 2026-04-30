"""
Step 26: Energy Grid Optimization (QUBO)
Solving energy grid problems with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def grid_optimization_qubo(generators, loads, lines):
    """
    QUBO for simplified grid optimization
    
    generators: list of (id, cost, capacity)
    loads: dict of load_id -> demand
    lines: list of (gen_id, load_id) connections
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    demand_penalty = 50
    cost_penalty = 1
    
    for gen_id, cost, cap in generators:
        linear[gen_id] = cost * cost_penalty
    
    for gen_id, cost, cap in generators:
        quadratic[(gen_id, gen_id)] = demand_penalty * cap * cap
    
    for i, (gen1, cost1, cap1) in enumerate(generators):
        for j, (gen2, cost2, cap2) in enumerate(generators):
            if i < j:
                quadratic[(gen1, gen2)] = demand_penalty * 2 * cap1 * cap2
    
    offset = demand_penalty * sum(loads.values()) * sum(loads.values())
    
    for gen_id, _, cap in generators:
        linear[gen_id] += -2 * demand_penalty * sum(loads.values()) * cap
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, generators, loads


def solve_grid_optimization(generators, loads, lines):
    """Solve grid optimization"""
    
    print("=" * 60)
    print("Step 26: Energy Grid Optimization (QUBO)")
    print("=" * 60)
    
    print(f"\nGenerators: {generators}")
    print(f"Loads: {loads}")
    
    bqm, generators, loads = grid_optimization_qubo(generators, loads, lines)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    total_generation = sum(best_state.get(gen[0], 0) * gen[2] for gen in generators)
    total_demand = sum(loads.values())
    
    print(f"Total generation: {total_generation}")
    print(f"Total demand: {total_demand}")
    
    return best_state, best_cost, total_generation


def simple_grid():
    """Simple grid"""
    
    print("\n1. Simple Grid")
    print("-" * 40)
    
    generators = [('G1', 10, 50), ('G2', 15, 30), ('G3', 20, 40)]
    loads = {'L1': 40, 'L2': 30}
    lines = [('G1', 'L1'), ('G2', 'L1'), ('G3', 'L2')]
    
    return solve_grid_optimization(generators, loads, lines)


def regional_grid():
    """Regional grid"""
    
    print("\n2. Regional Grid")
    print("-" * 40)
    
    generators = [
        ('coal', 25, 100),
        ('gas', 40, 60),
        ('solar', 10, 80),
        ('hydro', 30, 50)
    ]
    loads = {'city_a': 80, 'city_b': 60, 'city_c': 50}
    lines = [('coal', 'city_a'), ('gas', 'city_a'), ('solar', 'city_b'), ('hydro', 'city_c')]
    
    return solve_grid_optimization(generators, loads, lines)


if __name__ == "__main__":
    simple_grid()
    regional_grid()