"""
Step 14: Feature Selection (QUBO)
Selecting optimal features for ML models
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def feature_selection_qubo(feature_scores, feature_correlations, num_features_to_select):
    """
    Create QUBO for feature selection
    
    feature_scores: dict of feature -> relevance score
    feature_correlations: dict of (i, j) -> correlation
    num_features_to_select: number of features to select
    """
    
    features = list(feature_scores.keys())
    n = len(features)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    selection_penalty = 100
    redundancy_penalty = 10
    
    for i, feat in enumerate(features):
        linear[feat] = -feature_scores.get(feat, 1)
    
    for i in range(n):
        for j in range(i + 1, n):
            feat_i = features[i]
            feat_j = features[j]
            corr = feature_correlations.get((feat_i, feat_j), 0)
            if corr == 0:
                corr = feature_correlations.get((feat_j, feat_i), 0)
            quadratic[(feat_i, feat_j)] = redundancy_penalty * corr
    
    for i, feat in enumerate(features):
        quadratic[(feat, feat)] = -2 * selection_penalty * num_features_to_select
    
    for i in range(n):
        for j in range(n):
            if i != j:
                pass
    
    offset = selection_penalty * num_features_to_select * num_features_to_select
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, features


def solve_feature_selection(feature_scores, feature_correlations, num_features_to_select):
    """Solve feature selection"""
    
    print("=" * 60)
    print("Step 14: Feature Selection (QUBO)")
    print("=" * 60)
    
    print(f"\nFeatures: {list(feature_scores.keys())}")
    print(f"Select: {num_features_to_select}")
    
    bqm, features = feature_selection_qubo(feature_scores, feature_correlations, num_features_to_select)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    selected = [f for f in features if best_state.get(f, 0) == 1]
    print(f"Selected features: {selected}")
    print(f"Count: {len(selected)}")
    
    total_score = sum(feature_scores.get(f, 0) for f in selected)
    print(f"Total relevance: {total_score}")
    
    return best_state, best_cost, selected


def simple_feature_selection():
    """Simple feature selection"""
    
    print("\n1. Simple Feature Selection")
    print("-" * 40)
    
    feature_scores = {
        'f1': 10,
        'f2': 8,
        'f3': 6,
        'f4': 5,
        'f5': 3
    }
    feature_correlations = {
        ('f1', 'f2'): 0.8,
        ('f1', 'f3'): 0.2,
        ('f2', 'f3'): 0.7,
        ('f3', 'f4'): 0.6,
        ('f4', 'f5'): 0.9
    }
    num_features_to_select = 3
    
    return solve_feature_selection(feature_scores, feature_correlations, num_features_to_select)


def high_correlation_case():
    """Feature selection with high correlations"""
    
    print("\n2. High Correlation Case")
    print("-" * 40)
    
    feature_scores = {
        'A': 10,
        'B': 9,
        'C': 8,
        'D': 2
    }
    feature_correlations = {
        ('A', 'B'): 0.95,
        ('A', 'C'): 0.3,
        ('B', 'C'): 0.4,
        ('C', 'D'): 0.9
    }
    num_features_to_select = 2
    
    return solve_feature_selection(feature_scores, feature_correlations, num_features_to_select)


def medical_features():
    """Medical feature selection"""
    
    print("\n3. Medical Feature Selection")
    print("-" * 40)
    
    feature_scores = {
        'age': 9,
        'blood_pressure': 8,
        'cholesterol': 7,
        'weight': 6,
        'height': 4,
        'smoking': 8,
        'exercise': 5,
        'diet': 6
    }
    feature_correlations = {
        ('age', 'blood_pressure'): 0.7,
        ('weight', 'cholesterol'): 0.8,
        ('weight', 'height'): 0.3,
        ('smoking', 'blood_pressure'): 0.5,
        ('exercise', 'weight'): 0.6,
        ('diet', 'cholesterol'): 0.7,
        ('age', 'weight'): 0.4
    }
    num_features_to_select = 4
    
    return solve_feature_selection(feature_scores, feature_correlations, num_features_to_select)


def classification_features():
    """Binary classification features"""
    
    print("\n4. Binary Classification Features")
    print("-" * 40)
    
    feature_scores = {
        'feat_1': 10,
        'feat_2': 8,
        'feat_3': 7,
        'feat_4': 5,
        'feat_5': 3,
        'feat_6': 2
    }
    feature_correlations = {}
    for i in range(1, 7):
        for j in range(i + 1, 7):
            if abs(i - j) == 1:
                feature_correlations[(f'feat_{i}', f'feat_{j}')] = 0.8
            else:
                feature_correlations[(f'feat_{i}', f'feat_{j}')] = 0.1
    
    num_features_to_select = 3
    
    return solve_feature_selection(feature_scores, feature_correlations, num_features_to_select)


if __name__ == "__main__":
    simple_feature_selection()
    high_correlation_case()
    medical_features()
    classification_features()