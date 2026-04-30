"""
Step 13: Clustering (QUBO)
Solving clustering problems with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def clustering_qubo(points, num_clusters):
    """
    Create QUBO for clustering
    
    points: list of (x, y) coordinates
    num_clusters: number of clusters
    """
    
    n = len(points)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 50
    distance_penalty = 1
    
    for i in range(n):
        for c in range(num_clusters):
            linear[(i, c)] = 0
    
    for i in range(n):
        for c1 in range(num_clusters):
            for c2 in range(c1 + 1, num_clusters):
                var1 = (i, c1)
                var2 = (i, c2)
                quadratic[(var1, var2)] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    for c in range(num_clusters):
        for i in range(n):
            for j in range(i + 1, n):
                var_i = (i, c)
                var_j = (j, c)
                dist = ((points[i][0] - points[j][0])**2 + 
                        (points[i][1] - points[j][1])**2) ** 0.5
                quadratic[(var_i, var_j)] = quadratic.get((var_i, var_j), 0) + distance_penalty * dist
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, n


def solve_clustering(points, num_clusters):
    """Solve clustering problem"""
    
    print("=" * 60)
    print("Step 13: Clustering (QUBO)")
    print("=" * 60)
    
    n = len(points)
    print(f"\nPoints: {points}")
    print(f"Number of clusters: {num_clusters}")
    
    bqm, n = clustering_qubo(points, num_clusters)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1500, temp=12.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    clusters = {c: [] for c in range(num_clusters)}
    for i in range(n):
        for c in range(num_clusters):
            if best_state.get((i, c), 0) == 1:
                clusters[c].append(i)
                break
    
    print(f"Clusters: {clusters}")
    
    for c in range(num_clusters):
        if clusters[c]:
            centroid_x = sum(points[i][0] for i in clusters[c]) / len(clusters[c])
            centroid_y = sum(points[i][1] for i in clusters[c]) / len(clusters[c])
            print(f"Cluster {c}: points={clusters[c]}, centroid=({centroid_x:.2f}, {centroid_y:.2f})")
    
    return best_state, best_cost, clusters


def simple_3_cluster():
    """3 clearly separated clusters"""
    
    print("\n1. 3 Clearly Separated Clusters")
    print("-" * 40)
    
    points = [
        (0, 0), (1, 1), (0.5, 0.5),
        (10, 10), (11, 11), (10.5, 10.5),
        (20, 0), (21, 1), (20.5, 0.5)
    ]
    num_clusters = 3
    
    return solve_clustering(points, num_clusters)


def two_cluster_overlap():
    """Two clusters with some overlap"""
    
    print("\n2. Two Clusters with Overlap")
    print("-" * 40)
    
    points = [
        (1, 1), (2, 2), (1.5, 1.5),
        (5, 5), (6, 6), (5.5, 5.5),
        (3, 3)
    ]
    num_clusters = 2
    
    return solve_clustering(points, num_clusters)


def four_cluster():
    """Four clusters in 2D"""
    
    print("\n3. Four Clusters")
    print("-" * 40)
    
    points = [
        (0, 0), (1, 0), (0, 1),
        (10, 0), (11, 0), (10, 1),
        (0, 10), (1, 10), (0, 11),
        (10, 10), (11, 10), (10, 11)
    ]
    num_clusters = 4
    
    return solve_clustering(points, num_clusters)


def find_optimal_k():
    """Find optimal number of clusters"""
    
    print("\n4. Finding Optimal K")
    print("-" * 40)
    
    points = [
        (0, 0), (1, 1), (0.5, 0.5),
        (5, 5), (6, 5), (5.5, 6),
        (10, 0), (11, 1)
    ]
    
    print(f"Points: {points}")
    
    for k in [2, 3]:
        print(f"\n--- Testing k={k} ---")
        bqm, n = clustering_qubo(points, k)
        
        solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
        
        qubo, offset_val = bqm.to_qubo()
        best_state, best_cost = solver.solve(qubo)
        best_cost = best_cost + offset_val
        
        clusters = {c: [] for c in range(k)}
        for i in range(n):
            for c in range(k):
                if best_state.get((i, c), 0) == 1:
                    clusters[c].append(i)
        
        print(f"Solution energy: {best_cost}")
        print(f"Clusters: {clusters}")


if __name__ == "__main__":
    simple_3_cluster()
    two_cluster_overlap()
    four_cluster()
    find_optimal_k()