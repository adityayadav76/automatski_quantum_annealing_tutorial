"""
Step 11: Traveling Salesman Problem (QUBO)
Solving TSP with QUBO formulation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def tsp_qubo(distance_matrix):
    """
    Create QUBO for Traveling Salesman Problem
    
    distance_matrix: 2D matrix where distance_matrix[i][j] is distance from i to j
    """
    
    n = len(distance_matrix)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 100
    adjacency_penalty = 100
    
    for i in range(n):
        for t in range(n):
            linear[(i, t)] = 0
    
    for i in range(n):
        for t1 in range(n):
            for t2 in range(t1 + 1, n):
                var1 = (i, t1)
                var2 = (i, t2)
                quadratic[(var1, var2)] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    for t in range(n):
        for i in range(n):
            for j in range(i + 1, n):
                var_i = (i, t)
                var_j = (j, t)
                quadratic[(var_i, var_j)] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    for t in range(n - 1):
        for i in range(n):
            for j in range(n):
                if i != j:
                    var1 = (i, t)
                    var2 = (j, t + 1)
                    distance = distance_matrix[i][j]
                    quadratic[(var1, var2)] = 2 * distance
    
    for t in range(n - 1):
        for i in range(n):
            for j in range(n):
                if i != j:
                    offset += distance_matrix[i][j]
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, n


def solve_tsp(distance_matrix):
    """Solve TSP"""
    
    print("=" * 60)
    print("Step 11: Traveling Salesman Problem")
    print("=" * 60)
    
    n = len(distance_matrix)
    print(f"\nNumber of cities: {n}")
    print(f"Distance matrix: {distance_matrix}")
    
    bqm, n = tsp_qubo(distance_matrix)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=2000, temp=15.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy (total distance): {best_cost}")
    
    tour = []
    for t in range(n):
        for i in range(n):
            if best_state.get((i, t), 0) == 1:
                tour.append(i)
                break
    
    total_distance = 0
    for t in range(n - 1):
        total_distance += distance_matrix[tour[t]][tour[t + 1]]
    total_distance += distance_matrix[tour[-1]][tour[0]]
    
    print(f"Tour: {tour}")
    print(f"Total distance: {total_distance}")
    
    return best_state, best_cost, tour, total_distance


def three_cities():
    """Simple 3 city TSP"""
    
    print("\n1. 3 Cities")
    print("-" * 40)
    
    distance_matrix = [
        [0, 10, 15],
        [10, 0, 35],
        [15, 35, 0]
    ]
    
    return solve_tsp(distance_matrix)


def four_cities():
    """4 city symmetric TSP"""
    
    print("\n2. 4 Cities (Symmetric)")
    print("-" * 40)
    
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    return solve_tsp(distance_matrix)


def four_cities_asymmetric():
    """4 city asymmetric TSP"""
    
    print("\n3. 4 Cities (Asymmetric)")
    print("-" * 40)
    
    distance_matrix = [
        [0, 12, 10, 25],
        [8, 0, 15, 20],
        [7, 9, 0, 30],
        [20, 15, 25, 0]
    ]
    
    return solve_tsp(distance_matrix)


def five_cities():
    """5 city TSP"""
    
    print("\n4. 5 Cities")
    print("-" * 40)
    
    distance_matrix = [
        [0, 12, 10, 8, 15],
        [12, 0, 20, 15, 10],
        [10, 20, 0, 25, 12],
        [8, 15, 25, 0, 18],
        [15, 10, 12, 18, 0]
    ]
    
    return solve_tsp(distance_matrix)


def weighted_tsp():
    """TSP with different edge weights"""
    
    print("\n5. Weighted TSP")
    print("-" * 40)
    
    import random
    random.seed(42)
    
    n = 4
    distance_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                row.append(random.randint(5, 30))
        distance_matrix.append(row)
    
    for i in range(n):
        for j in range(n):
            distance_matrix[j][i] = distance_matrix[i][j]
    
    print(f"Distance matrix:\n{distance_matrix}")
    
    return solve_tsp(distance_matrix)


if __name__ == "__main__":
    three_cities()
    four_cities()
    four_cities_asymmetric()
    five_cities()
    weighted_tsp()