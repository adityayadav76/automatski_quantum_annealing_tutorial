"""
Step 10: Max-Cut Problem
Finding maximum cut in a graph
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def maxcut_qubo(edges):
    """
    Create QUBO for Max-Cut problem
    
    edges: list of (u, v) tuples representing edges
    """
    
    vertices = set()
    for u, v in edges:
        vertices.add(u)
        vertices.add(v)
    vertices = sorted(vertices)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    for vertex in vertices:
        linear[vertex] = 0
    
    for u, v in edges:
        linear[u] += -1
        linear[v] += -1
        quadratic[(u, v)] = 2
        
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, vertices


def solve_maxcut(edges):
    """Solve Max-Cut problem"""
    
    print("=" * 60)
    print("Step 10: Max-Cut Problem")
    print("=" * 60)
    
    print(f"\nEdges: {edges}")
    
    bqm, vertices = maxcut_qubo(edges)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    set_a = [v for v in vertices if best_state.get(v, 0) == 0]
    set_b = [v for v in vertices if best_state.get(v, 0) == 1]
    
    print(f"Set A: {set_a}")
    print(f"Set B: {set_b}")
    
    cut_size = sum(1 for u, v in edges if best_state.get(u, 0) != best_state.get(v, 0))
    print(f"Cut size: {cut_size}")
    
    return best_state, best_cost, set_a, set_b, cut_size


def simple_triangle():
    """Triangle (max cut = 2)"""
    
    print("\n1. Triangle Graph (max cut = 2)")
    print("-" * 40)
    
    edges = [(0, 1), (1, 2), (0, 2)]
    
    return solve_maxcut(edges)


def square_edges():
    """Square (max cut = 2)"""
    
    print("\n2. Square (max cut = 2)")
    print("-" * 40)
    
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    
    return solve_maxcut(edges)


def pentagon():
    """Pentagon (max cut = 3)"""
    
    print("\n3. Pentagon (max cut = 3)")
    print("-" * 40)
    
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    
    return solve_maxcut(edges)


def complete_graph_5():
    """Complete graph K5 (max cut = 10)"""
    
    print("\n4. Complete Graph K5 (max cut = 10)")
    print("-" * 40)
    
    edges = []
    for i in range(5):
        for j in range(i + 1, 5):
            edges.append((i, j))
    
    return solve_maxcut(edges)


def path_graph():
    """Path graph (max cut = n-1 for even n)"""
    
    print("\n5. Path Graph P5 (max cut = 4)")
    print("-" * 40)
    
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    
    return solve_maxcut(edges)


def star_graph():
    """Star graph with 5 leaves"""
    
    print("\n6. Star Graph (center + 5 leaves)")
    print("-" * 40)
    
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    
    return solve_maxcut(edges)


def weighted_maxcut():
    """Weighted Max-Cut"""
    
    print("\n7. Weighted Max-Cut")
    print("-" * 40)
    
    print("Edges with weights")
    
    weighted_edges = [
        (0, 1, 3),
        (1, 2, 1),
        (2, 3, 4),
        (3, 0, 2),
        (0, 2, 5),
        (1, 3, 3)
    ]
    
    vertices = set()
    for u, v, w in weighted_edges:
        vertices.add(u)
        vertices.add(v)
    vertices = sorted(vertices)
    
    linear = {v: 0 for v in vertices}
    quadratic = {}
    offset = 0
    
    for u, v, w in weighted_edges:
        linear[u] += -w
        linear[v] += -w
        quadratic[(u, v)] = 2 * w
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    set_a = [v for v in vertices if best_state.get(v, 0) == 0]
    set_b = [v for v in vertices if best_state.get(v, 0) == 1]
    
    print(f"Set A: {set_a}")
    print(f"Set B: {set_b}")
    
    total_weight = sum(w for u, v, w in weighted_edges if best_state.get(u, 0) != best_state.get(v, 0))
    print(f"Weighted cut value: {total_weight}")
    
    return best_state, best_cost


if __name__ == "__main__":
    simple_triangle()
    square_edges()
    pentagon()
    complete_graph_5()
    path_graph()
    star_graph()
    weighted_maxcut()