"""
Step 17: Vehicle Routing Problem (QUBO)
Solving VRP with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def vrp_qubo(customers, distances, num_vehicles):
    """
    Create QUBO for Vehicle Routing Problem
    
    customers: list of customer indices (0 is depot)
    distances: dict of (i, j) -> distance
    num_vehicles: number of vehicles available
    """
    
    n = len(customers) - 1
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 100
    route_penalty = 50
    
    for v in range(num_vehicles):
        for i in customers:
            linear[(v, i)] = 0
    
    for v in range(num_vehicles):
        for i in customers:
            for j in customers:
                if i != j:
                    distance = distances.get((i, j), distances.get((j, i), 1))
                    quadratic[((v, i), (v, j))] = quadratic.get(((v, i), (v, j)), 0) + distance
    
    for i in customers[1:]:
        for v1 in range(num_vehicles):
            for v2 in range(v1 + 1, num_vehicles):
                quadratic[((v1, i), (v2, i))] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, customers, num_vehicles


def solve_vrp(customers, distances, num_vehicles):
    """Solve VRP"""
    
    print("=" * 60)
    print("Step 17: Vehicle Routing (QUBO)")
    print("=" * 60)
    
    print(f"\nCustomers: {customers}")
    print(f"Number of vehicles: {num_vehicles}")
    
    bqm, customers, num_vehicles = vrp_qubo(customers, distances, num_vehicles)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=2000, temp=15.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution (excerpt): {dict(list(best_state.items())[:10])}")
    print(f"Energy: {best_cost}")
    
    routes = {v: [] for v in range(num_vehicles)}
    for (v, customer), value in best_state.items():
        if value == 1:
            routes[v].append(customer)
    
    for v in range(num_vehicles):
        routes[v] = sorted(routes[v])
    
    print(f"Routes: {routes}")
    
    total_distance = 0
    for v in range(num_vehicles):
        route = routes[v]
        if route:
            prev = 0
            for customer in route:
                total_distance += distances.get((prev, customer), distances.get((customer, prev), 1))
                prev = customer
            total_distance += distances.get((prev, 0), distances.get((0, prev), 1))
    
    print(f"Total distance: {total_distance}")
    
    return best_state, best_cost, routes, total_distance


def simple_vrp():
    """Simple VRP"""
    
    print("\n1. Simple VRP (3 customers, 2 vehicles)")
    print("-" * 40)
    
    customers = [0, 1, 2, 3]
    distances = {
        (0, 1): 10, (0, 2): 15, (0, 3): 20,
        (1, 2): 5, (1, 3): 10,
        (2, 3): 8
    }
    for i in range(4):
        for j in range(4):
            if (i, j) not in distances:
                distances[(i, j)] = distances.get((j, i), 1)
    
    num_vehicles = 2
    
    return solve_vrp(customers, distances, num_vehicles)


def four_customers_vrp():
    """VRP with 4 customers"""
    
    print("\n2. VRP with 4 Customers")
    print("-" * 40)
    
    customers = [0, 1, 2, 3, 4]
    distances = {
        (0, 1): 8, (0, 2): 12, (0, 3): 15, (0, 4): 10,
        (1, 2): 6, (1, 3): 8, (1, 4): 10,
        (2, 3): 5, (2, 4): 7,
        (3, 4): 6
    }
    for i in range(5):
        for j in range(5):
            if (i, j) not in distances:
                distances[(i, j)] = distances.get((j, i), 1)
    
    num_vehicles = 2
    
    return solve_vrp(customers, distances, num_vehicles)


def delivery_routes():
    """Daily delivery routes"""
    
    print("\n3. Daily Delivery Routes")
    print("-" * 40)
    
    customers = [0, 1, 2, 3, 4, 5]
    distances = {
        (0, 1): 5, (0, 2): 8, (0, 3): 12, (0, 4): 10, (0, 5): 15,
        (1, 2): 4, (1, 3): 8, (1, 4): 6, (1, 5): 10,
        (2, 3): 5, (2, 4): 7, (2, 5): 8,
        (3, 4): 3, (3, 5): 6,
        (4, 5): 7
    }
    for i in range(6):
        for j in range(6):
            if (i, j) not in distances:
                distances[(i, j)] = distances.get((j, i), 1)
    
    num_vehicles = 2
    
    return solve_vrp(customers, distances, num_vehicles)


def multi_depot_vrp():
    """Multi-depot VRP (simplified)"""
    
    print("\n4. Multi-Depot VRP")
    print("-" * 40)
    
    customers = [0, 1, 2, 3]
    distances = {
        (0, 1): 5, (0, 2): 8, (0, 3): 12,
        (1, 2): 6, (1, 3): 10,
        (2, 3): 7
    }
    for i in range(4):
        for j in range(4):
            if (i, j) not in distances:
                distances[(i, j)] = distances.get((j, i), 1)
    
    num_vehicles = 2
    
    return solve_vrp(customers, distances, num_vehicles)


if __name__ == "__main__":
    simple_vrp()
    four_customers_vrp()
    delivery_routes()
    multi_depot_vrp()