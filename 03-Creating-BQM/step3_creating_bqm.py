"""
Step 3: Creating Binary Quadratic Models (BQM)
Exploring different methods to create BQMs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def method_direct_constructor():
    """Method 1: Direct constructor"""
    
    print("=" * 60)
    print("Step 3: Creating BQM")
    print("=" * 60)
    
    print("\n1. Direct Constructor")
    print("-" * 40)
    
    linear = {'x': 1.0, 'y': 2.0, 'z': 0.5}
    quadratic = {('x', 'y'): -1.0, ('y', 'z'): -0.5}
    offset = 3.0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    print(f"Created BQM with {len(bqm)} variables")
    print(f"Linear: {dict(bqm.linear)}")
    print(f"Quadratic: {dict(bqm.quadratic)}")
    print(f"Offset: {bqm.offset}")
    
    return bqm


def method_from_qubo():
    """Method 2: From QUBO dictionary"""
    
    print("\n2. From QUBO Dictionary")
    print("-" * 40)
    
    Q = {
        ('x', 'x'): 1.0,
        ('x', 'y'): -2.0,
        ('y', 'y'): 1.5,
        ('y', 'z'): -1.0,
        ('z', 'z'): 2.0
    }
    
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
    
    print(f"Created BQM from QUBO")
    print(f"Variables: {list(bqm.variables)}")
    print(f"Linear: {dict(bqm.linear)}")
    print(f"Quadratic: {dict(bqm.quadratic)}")
    
    return bqm


def method_from_ising():
    """Method 3: From Ising model"""
    
    print("\n3. From Ising Model")
    print("-" * 40)
    
    h = {'s1': 0.5, 's2': -0.3, 's3': 0.8}
    J = {('s1', 's2'): 1.0, ('s2', 's3'): -0.5}
    
    bqm = dimod.BinaryQuadraticModel.from_ising(h, J)
    
    print(f"Created BQM from Ising")
    print(f"Variables: {list(bqm.variables)}")
    print(f"Linear (h): {dict(bqm.linear)}")
    print(f"Quadratic (J): {dict(bqm.quadratic)}")
    
    return bqm


def method_empty_bqm():
    """Method 4: Empty BQM with add operations"""
    
    print("\n4. Empty BQM with Add Operations")
    print("-" * 40)
    
    bqm = dimod.BinaryQuadraticModel.empty(dimod.BINARY)
    print(f"Empty BQM: {list(bqm.variables)}")
    
    bqm.add_variable('x', 1.0)
    print(f"After add_variable('x', 1.0): {list(bqm.variables)}")
    
    bqm.add_variable('y', 2.0)
    bqm.add_interaction('x', 'y', -1.5)
    print(f"After adding interactions: {list(bqm.variables)}")
    
    bqm.add_offset(5.0)
    print(f"Offset: {bqm.offset}")
    
    return bqm


def method_dict_update():
    """Method 5: Using add_variables_from dictionary"""
    
    print("\n5. Using add_variable/add_interaction")
    print("-" * 40)
    
    bqm = dimod.BinaryQuadraticModel.empty(dimod.BINARY)
    
    linear_dict = {'x': 1.0, 'y': 1.5}
    quadratic_dict = {('x', 'y'): -1.0}
    
    for var, bias in linear_dict.items():
        bqm.add_variable(var, bias)
    
    for (i, j), bias in quadratic_dict.items():
        bqm.add_interaction(i, j, bias)
    
    print(f"After adding variables: {dict(bqm.linear)}")
    print(f"Quadratic: {dict(bqm.quadratic)}")
    
    return bqm


def solve_bqm(bqm, name):
    """Solve and display BQM result"""
    
    print(f"\nSolving: {name}")
    print("-" * 40)
    
    solver = AutomatskiInitiumSASolver(
        host=HOST, 
        port=PORT, 
        max_iter=1000, 
        temp=10.0, 
        cooling_rate=0.01, 
        num_reads=10
    )
    
    qubo, offset = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset
    
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    return best_state, best_cost


def add_interactions_example():
    """Example: Add interactions with different methods"""
    
    print("\n6. Adding Interactions Efficiently")
    print("-" * 40)
    
    bqm = dimod.BinaryQuadraticModel({'a': 1, 'b': 1, 'c': 1}, {}, 0, dimod.BINARY)
    
    interactions = [
        ('a', 'b', -1),
        ('b', 'c', -1),
        ('a', 'c', -1)
    ]
    
    for i, j, weight in interactions:
        bqm.add_interaction(i, j, weight)
    
    print(f"Interactions: {dict(bqm.quadratic)}")
    
    return bqm


if __name__ == "__main__":
    bqm1 = method_direct_constructor()
    solve_bqm(bqm1, "Direct Constructor")
    
    bqm2 = method_from_qubo()
    solve_bqm(bqm2, "From QUBO")
    
    bqm3 = method_from_ising()
    solve_bqm(bqm3, "From Ising")
    
    bqm4 = method_empty_bqm()
    solve_bqm(bqm4, "Empty BQM")
    
    bqm5 = method_dict_update()
    solve_bqm(bqm5, "add_from")
    
    bqm6 = add_interactions_example()
    solve_bqm(bqm6, "Add Interactions")