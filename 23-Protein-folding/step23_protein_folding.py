"""
Step 23: Protein Folding (QUBO)
Solving simplified protein folding with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def protein_folding_qubo(sequence):
    """
    Simplified HP model for protein folding
    
    sequence: string of H (hydrophobic) and P (polar)
    """
    
    n = len(sequence)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    contact_penalty = 10
    connectivity_penalty = 20
    
    positions = [(x, y) for x in range(n) for y in range(n)]
    
    for i, pos_i in enumerate(positions[:n]):
        linear[(i, pos_i)] = 0
    
    for i in range(n):
        for pos1 in positions[:n]:
            for pos2 in positions[:n]:
                if pos1 != pos2:
                    quadratic[((i, pos1), (i, pos2))] = connectivity_penalty * 2
        offset += connectivity_penalty
    
    for pos in positions[:n]:
        for i in range(n):
            for j in range(i + 1, n):
                quadratic[((i, pos), (j, pos))] = connectivity_penalty * 2
        offset += connectivity_penalty
    
    for i in range(n - 1):
        for pos_i in positions[:n]:
            for pos_j in positions[:n]:
                dist = ((pos_i[0] - pos_j[0])**2 + (pos_i[1] - pos_j[1])**2) ** 0.5
                if dist == 1:
                    quadratic[((i, pos_i), (i+1, pos_j))] = -1
    
    for i in range(n):
        for j in range(i + 2, n):
            if sequence[i] == 'H' and sequence[j] == 'H':
                for pos_i in positions[:n]:
                    for pos_j in positions[:n]:
                        dist = ((pos_i[0] - pos_j[0])**2 + (pos_i[1] - pos_j[1])**2) ** 0.5
                        if dist < 1.5:
                            quadratic[((i, pos_i), (j, pos_j))] = contact_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, sequence


def solve_protein_folding(sequence):
    """Solve protein folding"""
    
    print("=" * 60)
    print("Step 23: Protein Folding (QUBO)")
    print("=" * 60)
    
    print(f"\nSequence: {sequence}")
    print("H = Hydrophobic, P = Polar")
    
    bqm, sequence = protein_folding_qubo(sequence)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=2000, temp=15.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution (excerpt): {dict(list(best_state.items())[:10])}")
    print(f"Energy: {best_cost}")
    
    print("\nNote: Full lattice solution requires more complex encoding.")
    print("This demonstrates the QUBO formulation concept.")
    
    return best_state, best_cost


def hp_sequence():
    """HP sequence folding"""
    
    print("\n1. HP Sequence (H=hydrophobic, P=polar)")
    print("-" * 40)
    
    sequence = "HHPH"
    
    return solve_protein_folding(sequence)


def longer_sequence():
    """Longer HP sequence"""
    
    print("\n2. Longer HP Sequence")
    print("-" * 40)
    
    sequence = "HPHPPH"
    
    return solve_protein_folding(sequence)


def hydrophobic_heavy():
    """Hydrophobic-heavy sequence"""
    
    print("\n3. Hydrophobic-Heavy Sequence")
    print("-" * 40)
    
    sequence = "HHHPHH"
    
    return solve_protein_folding(sequence)


if __name__ == "__main__":
    hp_sequence()
    longer_sequence()
    hydrophobic_heavy()