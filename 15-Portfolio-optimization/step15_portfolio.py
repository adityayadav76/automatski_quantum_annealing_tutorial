"""
Step 15: Portfolio Optimization (QUBO)
Solving portfolio optimization with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def portfolio_qubo(assets, returns, covariances, budget):
    """
    Create QUBO for portfolio optimization
    
    assets: list of asset names
    returns: dict of asset -> expected return
    covariances: dict of (i, j) -> covariance
    budget: number of assets to select
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    selection_penalty = 100
    risk_penalty = 1
    
    for asset in assets:
        linear[asset] = -returns.get(asset, 0)
    
    for i, asset_i in enumerate(assets):
        for j, asset_j in enumerate(assets):
            if i < j:
                cov = covariances.get((asset_i, asset_j), 0)
                if cov == 0:
                    cov = covariances.get((asset_j, asset_i), 0)
                quadratic[(asset_i, asset_j)] = risk_penalty * cov * 2
    
    for asset in assets:
        cov = covariances.get((asset, asset), 0)
        if cov == 0:
            cov = 0.1
        quadratic[(asset, asset)] = risk_penalty * cov
    
    for asset in assets:
        linear[asset] += -2 * selection_penalty * budget
    
    offset = selection_penalty * budget * budget
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, assets


def solve_portfolio(assets, returns, covariances, budget):
    """Solve portfolio optimization"""
    
    print("=" * 60)
    print("Step 15: Portfolio Optimization (QUBO)")
    print("=" * 60)
    
    print(f"\nAssets: {assets}")
    print(f"Budget (select {budget} assets)")
    print(f"Returns: {returns}")
    
    bqm, assets = portfolio_qubo(assets, returns, covariances, budget)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    selected = [a for a in assets if best_state.get(a, 0) == 1]
    print(f"Selected assets: {selected}")
    
    total_return = sum(returns.get(a, 0) for a in selected)
    print(f"Expected return: {total_return}")
    
    portfolio_variance = 0
    for i, a1 in enumerate(selected):
        for j, a2 in enumerate(selected):
            if i <= j:
                cov = covariances.get((a1, a2), 0)
                if cov == 0:
                    cov = covariances.get((a2, a1), 0)
                weight = 1 if i == j else 2
                portfolio_variance += weight * cov
    
    print(f"Portfolio variance (risk): {portfolio_variance:.2f}")
    
    return best_state, best_cost, selected, total_return


def simple_portfolio():
    """Simple portfolio selection"""
    
    print("\n1. Simple Portfolio (5 assets, select 2)")
    print("-" * 40)
    
    assets = ['A', 'B', 'C', 'D', 'E']
    returns = {'A': 10, 'B': 8, 'C': 12, 'D': 6, 'E': 9}
    covariances = {
        ('A', 'B'): 2, ('A', 'C'): 1, ('A', 'D'): 3, ('A', 'E'): 1,
        ('B', 'C'): 2, ('B', 'D'): 1, ('B', 'E'): 3,
        ('C', 'D'): 1, ('C', 'E'): 2,
        ('D', 'E'): 1
    }
    budget = 2
    
    return solve_portfolio(assets, returns, covariances, budget)


def diverse_portfolio():
    """Portfolio with diverse risk profiles"""
    
    print("\n2. Diverse Risk Portfolio")
    print("-" * 40)
    
    assets = ['stocks', 'bonds', 'real_estate', 'commodities', 'crypto']
    returns = {
        'stocks': 12,
        'bonds': 5,
        'real_estate': 8,
        'commodities': 15,
        'crypto': 25
    }
    covariances = {
        ('stocks', 'bonds'): 0.2,
        ('stocks', 'real_estate'): 0.5,
        ('stocks', 'commodities'): 0.6,
        ('stocks', 'crypto'): 0.7,
        ('bonds', 'real_estate'): 0.1,
        ('bonds', 'commodities'): 0.0,
        ('bonds', 'crypto'): 0.1,
        ('real_estate', 'commodities'): 0.3,
        ('real_estate', 'crypto'): 0.4,
        ('commodities', 'crypto'): 0.5
    }
    budget = 3
    
    return solve_portfolio(assets, returns, covariances, budget)


def balanced_portfolio():
    """Balanced investment portfolio"""
    
    print("\n3. Balanced Portfolio")
    print("-" * 40)
    
    assets = ['tech', 'healthcare', 'finance', 'energy', 'utilities', 'consumer']
    returns = {
        'tech': 15,
        'healthcare': 10,
        'finance': 8,
        'energy': 12,
        'utilities': 6,
        'consumer': 9
    }
    covariances = {
        ('tech', 'healthcare'): 0.4,
        ('tech', 'finance'): 0.5,
        ('tech', 'energy'): 0.3,
        ('tech', 'utilities'): 0.2,
        ('tech', 'consumer'): 0.4,
        ('healthcare', 'finance'): 0.3,
        ('healthcare', 'energy'): 0.2,
        ('healthcare', 'utilities'): 0.3,
        ('healthcare', 'consumer'): 0.4,
        ('finance', 'energy'): 0.4,
        ('finance', 'utilities'): 0.5,
        ('finance', 'consumer'): 0.5,
        ('energy', 'utilities'): 0.3,
        ('energy', 'consumer'): 0.2,
        ('utilities', 'consumer'): 0.4
    }
    budget = 3
    
    return solve_portfolio(assets, returns, covariances, budget)


def max_return_portfolio():
    """Focus on maximizing return"""
    
    print("\n4. Max Return Focus")
    print("-" * 40)
    
    assets = ['fund1', 'fund2', 'fund3', 'fund4', 'fund5']
    returns = {'fund1': 20, 'fund2': 15, 'fund3': 12, 'fund4': 10, 'fund5': 8}
    covariances = {
        ('fund1', 'fund2'): 3, ('fund1', 'fund3'): 2, ('fund1', 'fund4'): 1, ('fund1', 'fund5'): 1,
        ('fund2', 'fund3'): 3, ('fund2', 'fund4'): 2, ('fund2', 'fund5'): 1,
        ('fund3', 'fund4'): 2, ('fund3', 'fund5'): 2,
        ('fund4', 'fund5'): 3
    }
    budget = 2
    
    return solve_portfolio(assets, returns, covariances, budget)


if __name__ == "__main__":
    simple_portfolio()
    diverse_portfolio()
    balanced_portfolio()
    max_return_portfolio()