"""
Step 24: Cryptanalysis (QUBO)
Solving cryptanalysis problems with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def substitution_cipher_qubo(ciphertext, word_list):
    """
    QUBO for substitution cipher using dictionary matching
    
    ciphertext: encrypted text
    word_list: list of possible words
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    match_penalty = 10
    
    for i, word in enumerate(word_list):
        linear[f'word_{i}'] = 0
    
    for i, word1 in enumerate(word_list):
        for j, word2 in enumerate(word_list):
            if i < j:
                quadratic[(f'word_{i}', f'word_{j}')] = match_penalty * 2
        offset += match_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, word_list


def frequency_match_qubo(ciphertext, freq_map):
    """
    Frequency-based matching QUBO
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    penalty = 5
    
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        linear[letter] = 0
    
    cipher_counts = {}
    for char in ciphertext.lower():
        if char.isalpha():
            cipher_counts[char] = cipher_counts.get(char, 0) + 1
    
    target_freq = freq_map
    
    for cipher_letter, count in cipher_counts.items():
        for target_letter, target_count in target_freq.items():
            diff = abs(count / len(ciphertext) - target_count)
            linear[cipher_letter] += penalty * diff
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm


def solve_substitution_cipher(ciphertext, word_list):
    """Solve substitution cipher"""
    
    print("=" * 60)
    print("Step 24: Cryptanalysis (QUBO)")
    print("=" * 60)
    
    print(f"\nCiphertext: {ciphertext}")
    
    bqm, word_list = substitution_cipher_qubo(ciphertext, word_list)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    return best_state, best_cost


def simple_cipher():
    """Simple cipher example"""
    
    print("\n1. Simple Word Matching")
    print("-" * 40)
    
    ciphertext = "KHOOR"
    word_list = ["HELLO", "WORLD", "TEST", "CODE"]
    
    return solve_substitution_cipher(ciphertext, word_list)


def letter_frequency():
    """Letter frequency analysis"""
    
    print("\n2. Letter Frequency Analysis")
    print("-" * 40)
    
    ciphertext = "KHOOR ZRUOG"
    
    english_freq = {'a': 0.0817, 'b': 0.0149, 'c': 0.0278, 'd': 0.0423, 'e': 0.1270,
                    'f': 0.0223, 'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015,
                    'k': 0.0077, 'l': 0.0403, 'm': 0.0267, 'n': 0.0679, 'o': 0.0751,
                    'p': 0.0193, 'q': 0.0010, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
                    'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015, 'y': 0.0197,
                    'z': 0.0007}
    
    bqm = frequency_match_qubo(ciphertext, english_freq)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"Ciphertext: {ciphertext}")
    print(f"Solution: {best_state}")
    print(f"Energy: {best_cost}")
    
    return best_state, best_cost


def pattern_matching():
    """Pattern-based cryptanalysis"""
    
    print("\n3. Pattern Matching")
    print("-" * 40)
    
    ciphertext = "ABBA ABAB"
    patterns = ["HELLO", "WORLD", "TEST", "SEES", "LOOK"]
    
    return solve_substitution_cipher(ciphertext, patterns)


if __name__ == "__main__":
    simple_cipher()
    letter_frequency()
    pattern_matching()