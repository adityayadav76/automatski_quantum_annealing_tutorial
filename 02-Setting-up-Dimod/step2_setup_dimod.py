"""
Step 2: Setting up Dimod
Exploring Dimod library and BinaryQuadraticModel basics
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def create_basic_bqm():
    """Create and explore a basic BQM"""
    
    print("=" * 60)
    print("Step 2: Setting up Dimod")
    print("=" * 60)
    
    print("\n1. Creating a Basic BinaryQuadraticModel")
    print("-" * 40)
    
    linear = {'x': 1.0, 'y': 2.0}
    quadratic = {('x', 'y'): -1.0}
    offset = 0.0
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    print(f"Variables: {list(bqm.variables)}")
    print(f"Linear terms: {dict(bqm.linear)}")
    print(f"Quadratic terms: {dict(bqm.quadratic)}")
    print(f"Offset: {bqm.offset}")
    print(f"Vartype: {bqm.vartype}")
    
    return bqm


def explore_bqm_properties(bqm):
    """Explore various BQM properties and methods"""
    
    print("\n2. Exploring BQM Properties")
    print("-" * 40)
    
    print(f"Number of variables: {len(bqm)}")
    print(f"Has quadratic terms: {len(bqm.quadratic) > 0}")
    print(f"Number of interactions: {bqm.num_interactions}")
    
    print("\n3. BQM Methods")
    print("-" * 40)
    
    print(f"to_qubo() returns: Q matrix and offset")
    qubo, offset = bqm.to_qubo()
    print(f"  QUBO dict: {qubo}")
    print(f"  Offset: {offset}")
    
    print(f"\nto_ising() returns: h (linear), J (quadratic), offset")
    h, J, offset = bqm.to_ising()
    print(f"  h: {h}")
    print(f"  J: {J}")
    print(f"  Offset: {offset}")
    
    return qubo, offset


def modify_bqm():
    """Demonstrate modifying a BQM"""
    
    print("\n4. Modifying BQM")
    print("-" * 40)
    
    bqm = dimod.BinaryQuadraticModel({'x': 1}, {}, 0.0, vartype=dimod.BINARY)
    print(f"Initial: {dict(bqm.linear)}")
    
    bqm.add_variable('y', 2.0)
    print(f"After adding y: {dict(bqm.linear)}")
    
    bqm.add_interaction('x', 'y', -1.0)
    print(f"After adding interaction: {dict(bqm.quadratic)}")
    
    bqm.add_offset(5.0)
    print(f"After adding offset: {bqm.offset}")
    
    return bqm


def solve_simple_bqm(bqm):
    """Solve the BQM using the solver"""
    
    print("\n5. Solving the BQM")
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


def demonstrate_spin_variables():
    """Demonstrate SPIN vartype (variables in {-1, +1})"""
    
    print("\n6. SPIN Variables (values in {-1, +1})")
    print("-" * 40)
    
    linear = {'s1': 0.5, 's2': -0.3}
    quadratic = {('s1', 's2'): 0.8}
    offset = 1.0
    
    bqm_spin = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.SPIN)
    
    print(f"SPIN BQM created with vartype: {bqm_spin.vartype}")
    print(f"Linear: {dict(bqm_spin.linear)}")
    print(f"Quadratic: {dict(bqm_spin.quadratic)}")
    
    return bqm_spin


if __name__ == "__main__":
    bqm = create_basic_bqm()
    explore_bqm_properties(bqm)
    bqm = modify_bqm()
    solve_simple_bqm(bqm)
    demonstrate_spin_variables()