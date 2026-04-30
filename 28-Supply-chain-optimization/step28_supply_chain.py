"""
Step 28: Supply Chain Optimization (QUBO)
Solving supply chain problems with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def supply_chain_qubo(suppliers, products, demand):
    """
    QUBO for supply chain optimization
    
    suppliers: list of supplier names
    products: list of product types
    demand: dict of product -> demand
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    demand_penalty = 50
    cost_penalty = 1
    
    for supplier in suppliers:
        for product in products:
            linear[(supplier, product)] = cost_penalty
    
    for product in products:
        for s1, sup1 in enumerate(suppliers):
            for s2, sup2 in enumerate(suppliers):
                if s1 < s2:
                    quadratic[((sup1, product), (sup2, product))] = demand_penalty * 2
            offset += demand_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, suppliers, products


def solve_supply_chain(suppliers, products, demand):
    """Solve supply chain"""
    
    print("=" * 60)
    print("Step 28: Supply Chain Optimization (QUBO)")
    print("=" * 60)
    
    print(f"\nSuppliers: {suppliers}")
    print(f"Products: {products}")
    print(f"Demand: {demand}")
    
    bqm, suppliers, products = supply_chain_qubo(suppliers, products, demand)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    assignments = {}
    for supplier in suppliers:
        assignments[supplier] = []
        for product in products:
            if best_state.get((supplier, product), 0) == 1:
                assignments[supplier].append(product)
    
    print(f"Assignments: {assignments}")
    
    return best_state, best_cost, assignments


def simple_supply_chain():
    """Simple supply chain"""
    
    print("\n1. Simple Supply Chain")
    print("-" * 40)
    
    suppliers = ['S1', 'S2', 'S3']
    products = ['P1', 'P2']
    demand = {'P1': 100, 'P2': 80}
    
    return solve_supply_chain(suppliers, products, demand)


def multi_product_chain():
    """Multi-product supply chain"""
    
    print("\n2. Multi-Product Supply Chain")
    print("-" * 40)
    
    suppliers = ['Supplier_A', 'Supplier_B', 'Supplier_C']
    products = ['Component_1', 'Component_2', 'Component_3', 'Material_1']
    demand = {'Component_1': 50, 'Component_2': 30, 'Component_3': 40, 'Material_1': 100}
    
    return solve_supply_chain(suppliers, products, demand)


if __name__ == "__main__":
    simple_supply_chain()
    multi_product_chain()