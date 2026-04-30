"""
Solver utilities for Quantum Annealing Tutorial
Provides reusable functions for creating and solving QUBO problems
"""

import dimod
import numpy as np
from AutomatskiInitium import AutomatskiInitiumSASolver


HOST = "168.220.234.162"
PORT = 80
DEFAULT_MAX_ITER = 1000
DEFAULT_TEMP = 10.0
DEFAULT_COOLING_RATE = 0.01
DEFAULT_NUM_READS = 10


class QUBOSolver:
    """Wrapper class for solving QUBO problems using AutomatskiInitium solver"""
    
    def __init__(self, host=HOST, port=PORT, max_iter=DEFAULT_MAX_ITER,
                 temp=DEFAULT_TEMP, cooling_rate=DEFAULT_COOLING_RATE,
                 num_reads=DEFAULT_NUM_READS):
        self.solver = AutomatskiInitiumSASolver(
            host=host, port=port, max_iter=max_iter, temp=temp,
            cooling_rate=cooling_rate, num_reads=num_reads
        )
    
    def solve(self, bqm):
        """Solve a BinaryQuadraticModel and return (solution, energy)"""
        qubo, offset = bqm.to_qubo()
        best_state, best_cost = self.solver.solve(qubo)
        best_cost = best_cost + offset
        return best_state, best_cost


def create_bqm(linear, quadratic, offset=0.0, vartype=dimod.BINARY):
    """Create a BinaryQuadraticModel from linear and quadratic terms"""
    return dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype)


def solve_qubo(linear, quadratic, offset=0.0):
    """Quick function to solve a QUBO problem directly"""
    bqm = create_bqm(linear, quadratic, offset)
    solver = QUBOSolver()
    return solver.solve(bqm)


def add_penalty(bqm, variables, weight=10.0, penalty_type='one_hot'):
    """Add penalty terms to enforce constraints"""
    if penalty_type == 'one_hot':
        for i, var_i in enumerate(variables):
            for j, var_j in enumerate(variables):
                if i < j:
                    bqm.add_interaction(var_i, var_j, weight)
        bqm.add_offset(weight * len(variables))
    elif penalty_type == 'sum':
        for i, var_i in enumerate(variables):
            for j, var_j in enumerate(variables):
                if i < j:
                    bqm.add_interaction(var_i, var_j, 2 * weight)
        for var in variables:
            bqm.add_variable(var, -weight)
        bqm.add_offset(weight * len(variables))
    return bqm


def create_one_hot(n, prefix='x'):
    """Create variables for one-hot encoding of n options"""
    return [f'{prefix}_{i}' for i in range(n)]


def evaluate_solution(bqm, solution):
    """Calculate the energy of a given solution"""
    energy = bqm.offset
    for var, value in solution.items():
        if var in bqm.linear:
            energy += bqm.linear[var] * value
        for neighbor in bqm.quadratic:
            if var in bqm.quadratic[neighbor]:
                energy += bqm.quadratic[neighbor][var] * value * solution.get(neighbor, 0)
    return energy