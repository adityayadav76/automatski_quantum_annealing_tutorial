"""
Step 19: Machine Learning with QUBO
Applying QUBO to ML problems
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def binary_classification_qubo(X, y):
    """
    QUBO for binary classification
    
    X: list of feature vectors
    y: list of labels (0 or 1)
    """
    
    n_features = len(X[0])
    n_samples = len(X)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    margin_penalty = 10
    
    for i in range(n_samples):
        margin = 2 * y[i] - 1
        
        for j in range(n_features):
            linear[f'w_{j}'] = linear.get(f'w_{j}', 0) + margin * X[i][j] * margin_penalty
        
        linear['b'] = linear.get('b', 0) + margin * margin_penalty
    
    for i in range(n_samples):
        for j1 in range(n_features):
            for j2 in range(n_features):
                w1 = f'w_{j1}'
                w2 = f'w_{j2}'
                quadratic[(w1, w2)] = quadratic.get((w1, w2), 0) + margin_penalty * X[i][j1] * X[i][j2]
        
        for j in range(n_features):
            quadratic[(f'w_{j}', 'b')] = quadratic.get((f'w_{j}', 'b'), 0) + 2 * margin_penalty * X[i][j]
        
        quadratic[('b', 'b')] = quadratic.get(('b', 'b'), 0) + margin_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, n_features


def solve_binary_classification(X, y, n_features):
    """Solve binary classification"""
    
    print("=" * 60)
    print("Step 19: Machine Learning (QUBO)")
    print("=" * 60)
    
    print(f"\nTraining samples: {len(X)}")
    print(f"Features: {n_features}")
    print(f"Labels: {y}")
    
    bqm, n_features = binary_classification_qubo(X, y)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    predictions = []
    for i in range(len(X)):
        score = best_state.get('b', 0)
        for j in range(n_features):
            score += best_state.get(f'w_{j}', 0) * X[i][j]
        pred = 1 if score >= 0 else 0
        predictions.append(pred)
    
    accuracy = sum(1 for p, t in zip(predictions, y) if p == t) / len(y)
    print(f"Predictions: {predictions}")
    print(f"Accuracy: {accuracy * 100:.1f}%")
    
    return best_state, best_cost, predictions, accuracy


def simple_linear_classifier():
    """Simple linear classifier"""
    
    print("\n1. Simple Linear Classifier")
    print("-" * 40)
    
    X = [
        [1, 0],
        [0, 1],
        [1, 1],
        [0, 0]
    ]
    y = [1, 1, 0, 0]
    
    return solve_binary_classification(X, y, 2)


def and_gate():
    """AND gate classification"""
    
    print("\n2. AND Gate Classification")
    print("-" * 40)
    
    X = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]
    y = [0, 0, 0, 1]
    
    return solve_binary_classification(X, y, 2)


def or_gate():
    """OR gate classification"""
    
    print("\n3. OR Gate Classification")
    print("-" * 40)
    
    X = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]
    y = [0, 1, 1, 1]
    
    return solve_binary_classification(X, y, 2)


def xor_gate():
    """XOR gate (non-linearly separable)"""
    
    print("\n4. XOR Gate Classification")
    print("-" * 40)
    
    print("Note: XOR is not linearly separable, QUBO will find best approximation")
    
    X = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]
    y = [0, 1, 1, 0]
    
    return solve_binary_classification(X, y, 2)


def three_feature_classifier():
    """3-feature classifier"""
    
    print("\n5. 3-Feature Classifier")
    print("-" * 40)
    
    X = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ]
    y = [1, 1, 1, 0]
    
    return solve_binary_classification(X, y, 3)


if __name__ == "__main__":
    simple_linear_classifier()
    and_gate()
    or_gate()
    xor_gate()
    three_feature_classifier()