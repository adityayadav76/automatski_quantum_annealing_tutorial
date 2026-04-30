"""
Step 9: Graph Coloring
Solving graph coloring with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def graph_coloring_qubo(edges, num_colors):
    """
    Create QUBO for graph coloring
    
    edges: list of (u, v) tuples
    num_colors: number of colors to use
    """
    
    vertices = set()
    for u, v in edges:
        vertices.add(u)
        vertices.add(v)
    vertices = sorted(vertices)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 10
    conflict_penalty = 20
    
    for vertex in vertices:
        for c in range(num_colors):
            var = (vertex, c)
            linear[var] = 0
    
    for vertex in vertices:
        for c1 in range(num_colors):
            for c2 in range(c1 + 1, num_colors):
                var1 = (vertex, c1)
                var2 = (vertex, c2)
                quadratic[(var1, var2)] = one_hot_penalty * 2
    
    for vertex in vertices:
        offset += one_hot_penalty
    
    for u, v in edges:
        for c in range(num_colors):
            var_u = (u, c)
            var_v = (v, c)
            quadratic[(var_u, var_v)] = conflict_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, vertices


def solve_graph_coloring(edges, num_colors):
    """Solve graph coloring problem"""
    
    print("=" * 60)
    print("Step 9: Graph Coloring")
    print("=" * 60)
    
    print(f"\nEdges: {edges}")
    print(f"Colors: {num_colors}")
    
    bqm, vertices = graph_coloring_qubo(edges, num_colors)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    coloring = {}
    for (vertex, color), value in best_state.items():
        if value == 1:
            if vertex not in coloring:
                coloring[vertex] = []
            coloring[vertex].append(color)
    
    print(f"Coloring: {coloring}")
    
    valid = True
    for u, v in edges:
        if u in coloring and v in coloring:
            if any(c in coloring[u] for c in coloring[v]):
                valid = False
                print(f"Conflict: {u} and {v}")
    
    print(f"Valid coloring: {valid}")
    
    return best_state, best_cost, coloring


def simple_triangle():
    """Triangle graph (3-colorable)"""
    
    print("\n1. Triangle Graph (3 colors)")
    print("-" * 40)
    
    edges = [(0, 1), (1, 2), (0, 2)]
    num_colors = 3
    
    return solve_graph_coloring(edges, num_colors)


def square_with_diagonal():
    """Square with diagonal (needs 3 colors)"""
    
    print("\n2. Square with Diagonal (3 colors)")
    print("-" * 40)
    
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    num_colors = 3
    
    return solve_graph_coloring(edges, num_colors)


def complete_graph_k4():
    """Complete graph K4 (4 colors needed)"""
    
    print("\n3. Complete Graph K4 (4 colors)")
    print("-" * 40)
    
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3),
        (2, 3)
    ]
    num_colors = 4
    
    return solve_graph_coloring(edges, num_colors)


def Petersen_graph():
    """Petersen graph (3-colorable)"""
    
    print("\n4. Petersen Graph (3 colors)")
    print("-" * 40)
    
    outer = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    spokes = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
    inner = [(5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
    
    edges = outer + spokes + inner
    num_colors = 3
    
    return solve_graph_coloring(edges, num_colors)


def map_coloring():
    """Map coloring (US states simplified)"""
    
    print("\n5. Map Coloring (4 colors)")
    print("-" * 40)
    
    edges = [
        ('CA', 'OR'), ('CA', 'NV'), ('CA', 'AZ'),
        ('OR', 'WA'), ('OR', 'ID'), ('OR', 'NV'),
        ('NV', 'ID'), ('NV', 'UT'), ('NV', 'AZ'),
        ('AZ', 'UT'), ('ID', 'WA'), ('ID', 'UT'),
        ('UT', 'WA')
    ]
    num_colors = 4
    
    bqm, vertices = graph_coloring_qubo(edges, num_colors)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    coloring = {}
    for (vertex, color), value in best_state.items():
        if value == 1:
            coloring[vertex] = color
    
    print(f"Coloring: {coloring}")
    
    valid = True
    for u, v in edges:
        if u in coloring and v in coloring:
            if coloring[u] == coloring[v]:
                valid = False
                print(f"Conflict: {u} and {v}")
    
    print(f"Valid: {valid}")
    
    return best_state, best_cost, coloring


if __name__ == "__main__":
    simple_triangle()
    square_with_diagonal()
    complete_graph_k4()
    Petersen_graph()
    map_coloring()