"""
Step 12: Satisfiability Problems (QUBO)
Solving SAT problems with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def clause_to_qubo(literals):
    """
    Convert a clause to QUBO penalty
    
    literals: list of (variable, is_positive) tuples
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    penalty = 10
    
    variables = list(set(l[0] for l in literals))
    
    if len(literals) == 1:
        var, is_pos = literals[0]
        if is_pos:
            linear[var] = penalty
            offset += penalty
        else:
            linear[var] = -penalty
            offset += 0
    
    elif len(literals) == 2:
        var1, is_pos1 = literals[0]
        var2, is_pos2 = literals[1]
        
        if is_pos1 and is_pos2:
            quadratic[(var1, var2)] = penalty
            linear[var1] = penalty
            linear[var2] = penalty
            offset += penalty
        elif not is_pos1 and not is_pos2:
            quadratic[(var1, var2)] = penalty
            linear[var1] = -penalty
            linear[var2] = -penalty
            offset += 0
        elif is_pos1 and not is_pos2:
            quadratic[(var1, var2)] = -penalty
            linear[var1] = 0
            linear[var2] = penalty
            offset += penalty
        else:
            quadratic[(var1, var2)] = -penalty
            linear[var1] = penalty
            linear[var2] = 0
            offset += penalty
    
    elif len(literals) == 3:
        linear = {}
        quadratic = {}
        offset = 0
        penalty = 10
        
        for var, is_pos in literals:
            if is_pos:
                linear[var] = 1
            else:
                linear[var] = -1
        
        quadratic[('a', 'b')] = 2
        quadratic[('a', 'c')] = 2
        quadratic[('b', 'c')] = 2
        
        linear['a'] = 0
        linear['b'] = 0
        linear['c'] = 0
        offset = -3
        
        variables = ['a', 'b', 'c']
        for var in variables:
            if var not in linear:
                linear[var] = 0
        
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i < j:
                    if (var1, var2) not in quadratic:
                        quadratic[(var1, var2)] = 2
    
    return linear, quadratic, offset


def sat_qubo(clauses, variables):
    """
    Create QUBO for SAT problem
    
    clauses: list of clauses, each clause is list of (var, is_positive) tuples
    variables: list of variable names
    """
    
    penalty = 10
    
    linear = {v: 0 for v in variables}
    quadratic = {}
    offset = 0
    
    for clause in clauses:
        clause_vars = list(set(l[0] for l in clause))
        
        if len(clause) == 1:
            var, is_pos = clause[0]
            if is_pos:
                linear[var] += penalty
                offset += penalty
            else:
                linear[var] += -penalty
        
        elif len(clause) == 2:
            var1, is_pos1 = clause[0]
            var2, is_pos2 = clause[1]
            
            if is_pos1 and is_pos2:
                quadratic[(var1, var2)] = quadratic.get((var1, var2), 0) + penalty
                linear[var1] += penalty
                linear[var2] += penalty
                offset += penalty
            elif not is_pos1 and not is_pos2:
                quadratic[(var1, var2)] = quadratic.get((var1, var2), 0) + penalty
                linear[var1] += -penalty
                linear[var2] += -penalty
            elif is_pos1 and not is_pos2:
                quadratic[(var1, var2)] = quadratic.get((var1, var2), 0) - penalty
                linear[var2] += penalty
                offset += penalty
            else:
                quadratic[(var1, var2)] = quadratic.get((var1, var2), 0) - penalty
                linear[var1] += penalty
                offset += penalty
        
        elif len(clause) == 3:
            var1, is_pos1 = clause[0]
            var2, is_pos2 = clause[1]
            var3, is_pos3 = clause[2]
            
            for i, (v1, p1) in enumerate([(var1, is_pos1), (var2, is_pos2), (var3, is_pos3)]):
                for j, (v2, p2) in enumerate([(var1, is_pos1), (var2, is_pos2), (var3, is_pos3)]):
                    if i < j:
                        coeff = 1 if p1 and p2 else (-1 if not p1 and not p2 else 0)
                        if coeff != 0:
                            key = (v1, v2) if v1 < v2 else (v2, v1)
                            quadratic[key] = quadratic.get(key, 0) + penalty * coeff
            
            for v, is_pos in clause:
                if is_pos:
                    linear[v] += penalty
                else:
                    linear[v] += -penalty
            offset += penalty * 2
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm


def solve_sat(clauses, variables):
    """Solve SAT problem"""
    
    print("=" * 60)
    print("Step 12: Satisfiability (QUBO)")
    print("=" * 60)
    
    print(f"\nClauses: {clauses}")
    print(f"Variables: {variables}")
    
    bqm = sat_qubo(clauses, variables)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    print("\nChecking each clause:")
    satisfied = True
    for i, clause in enumerate(clauses):
        clause_satisfied = False
        for var, is_pos in clause:
            val = best_state.get(var, 0)
            if is_pos and val == 1:
                clause_satisfied = True
            elif not is_pos and val == 0:
                clause_satisfied = True
        
        status = "SATISFIED" if clause_satisfied else "UNSATISFIED"
        print(f"  Clause {i+1}: {clause} -> {status}")
        if not clause_satisfied:
            satisfied = False
    
    print(f"\nAll clauses satisfied: {satisfied}")
    
    return best_state, best_cost, satisfied


def simple_or():
    """Simple OR clause"""
    
    print("\n1. Simple OR (x OR y)")
    print("-" * 40)
    
    clauses = [[('x', True), ('y', True)]]
    variables = ['x', 'y']
    
    return solve_sat(clauses, variables)


def two_clauses():
    """Two clauses"""
    
    print("\n2. Two Clauses (x OR y, NOT x OR z)")
    print("-" * 40)
    
    clauses = [
        [('x', True), ('y', True)],
        [('x', False), ('z', True)]
    ]
    variables = ['x', 'y', 'z']
    
    return solve_sat(clauses, variables)


def three_sat_style():
    """3-SAT style problem"""
    
    print("\n3. 3-SAT Style (x OR y OR z, NOT x OR NOT y OR z)")
    print("-" * 40)
    
    clauses = [
        [('x', True), ('y', True), ('z', True)],
        [('x', False), ('y', False), ('z', True)]
    ]
    variables = ['x', 'y', 'z']
    
    return solve_sat(clauses, variables)


def unsatisfiable():
    """Clearly unsatisfiable case"""
    
    print("\n4. Unsatisfiable (x, NOT x)")
    print("-" * 40)
    
    clauses = [
        [('x', True)],
        [('x', False)]
    ]
    variables = ['x']
    
    return solve_sat(clauses, variables)


def larger_sat():
    """Larger SAT instance"""
    
    print("\n5. Larger SAT Instance")
    print("-" * 40)
    
    clauses = [
        [('a', True), ('b', True), ('c', True)],
        [('a', False), ('b', True)],
        [('b', False), ('c', True)],
        [('a', True), ('c', False)]
    ]
    variables = ['a', 'b', 'c']
    
    return solve_sat(clauses, variables)


def implication_graph():
    """Implication constraints"""
    
    print("\n6. Implication (if x then y, if y then z)")
    print("-" * 40)
    
    print("x -> y equivalent to NOT x OR y")
    print("y -> z equivalent to NOT y OR z")
    
    clauses = [
        [('x', False), ('y', True)],
        [('y', False), ('z', True)]
    ]
    variables = ['x', 'y', 'z']
    
    return solve_sat(clauses, variables)


if __name__ == "__main__":
    simple_or()
    two_clauses()
    three_sat_style()
    unsatisfiable()
    larger_sat()
    implication_graph()