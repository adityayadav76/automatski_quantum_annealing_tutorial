"""
Step 22: Route Optimization (QUBO)
Solving route optimization with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def route_qubo(nodes, edges, source, destination):
    """
    Create QUBO for route optimization
    
    nodes: list of node indices
    edges: dict of (u, v) -> cost
    source: source node
    destination: destination node
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    path_penalty = 100
    flow_penalty = 50
    
    for u, v in edges:
        linear[(u, v)] = edges[(u, v)]
    
    for node in nodes:
        if node != source and node != destination:
            outgoing = [e[1] for e in edges if e[0] == node]
            incoming = [e[0] for e in edges if e[1] == node]
            
            for i, out_u in enumerate(outgoing):
                for j, out_v in enumerate(outgoing):
                    if i < j:
                        quadratic[((node, out_u), (node, out_v))] = flow_penalty * 2
                offset += flow_penalty
            
            for i, in_u in enumerate(incoming):
                for j, in_v in enumerate(incoming):
                    if i < j:
                        quadratic[((in_u, node), (in_v, node))] = flow_penalty * 2
                offset += flow_penalty
    
    linear[(source, destination)] = -path_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, nodes, edges


def solve_route(nodes, edges, source, destination):
    """Solve route optimization"""
    
    print("=" * 60)
    print("Step 22: Route Optimization (QUBO)")
    print("=" * 60)
    
    print(f"\nNodes: {nodes}")
    print(f"Source: {source}, Destination: {destination}")
    
    bqm, nodes, edges = route_qubo(nodes, edges, source, destination)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1500, temp=12.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy (cost): {best_cost}")
    
    path = []
    current = source
    visited = {source}
    
    while current != destination:
        next_node = None
        for (u, v), cost in edges.items():
            if u == current and v not in visited:
                if best_state.get((u, v), 0) == 1:
                    next_node = v
                    break
        
        if next_node is None:
            for (u, v), cost in edges.items():
                if u == current and v not in visited:
                    next_node = v
                    break
        
        if next_node is None:
            break
        
        path.append(next_node)
        visited.add(next_node)
        current = next_node
    
    print(f"Path: {source} -> {' -> '.join(map(str, path))}")
    
    total_cost = sum(edges.get((path[i], path[i+1]), edges.get((path[i+1], path[i]), 0)) 
                     for i in range(len(path)-1)) if len(path) > 1 else 0
    
    if source in edges:
        for edge in edges:
            if edge[0] == source and edge[1] in path:
                total_cost += edges[edge]
    
    print(f"Total cost: {total_cost}")
    
    return best_state, best_cost, path, total_cost


def simple_route():
    """Simple route optimization"""
    
    print("\n1. Simple Route (4 nodes)")
    print("-" * 40)
    
    nodes = [0, 1, 2, 3]
    edges = {
        (0, 1): 5, (0, 2): 10, (1, 2): 3, 
        (1, 3): 15, (2, 3): 8
    }
    source = 0
    destination = 3
    
    return solve_route(nodes, edges, source, destination)


def city_route():
    """City route network"""
    
    print("\n2. City Route Network")
    print("-" * 40)
    
    nodes = [0, 1, 2, 3, 4]
    edges = {
        (0, 1): 10, (0, 2): 15, (1, 2): 5,
        (1, 3): 20, (2, 3): 8, (1, 4): 12,
        (2, 4): 6, (3, 4): 10
    }
    source = 0
    destination = 4
    
    return solve_route(nodes, edges, source, destination)


def delivery_route():
    """Delivery route optimization"""
    
    print("\n3. Delivery Route")
    print("-" * 40)
    
    nodes = ['depot', 'A', 'B', 'C', 'dest']
    edges = {
        ('depot', 'A'): 5, ('depot', 'B'): 8,
        ('A', 'B'): 3, ('A', 'C'): 6,
        ('B', 'C'): 4, ('B', 'dest'): 10,
        ('C', 'dest'): 7
    }
    source = 'depot'
    destination = 'dest'
    
    return solve_route(nodes, edges, source, destination)


def shortest_path():
    """Find shortest path"""
    
    print("\n4. Shortest Path")
    print("-" * 40)
    
    nodes = [0, 1, 2, 3, 4, 5]
    edges = {
        (0, 1): 4, (0, 2): 3, (1, 2): 1,
        (1, 3): 2, (2, 3): 4, (2, 4): 10,
        (3, 4): 7, (3, 5): 5, (4, 5): 8
    }
    source = 0
    destination = 5
    
    return solve_route(nodes, edges, source, destination)


if __name__ == "__main__":
    simple_route()
    city_route()
    delivery_route()
    shortest_path()