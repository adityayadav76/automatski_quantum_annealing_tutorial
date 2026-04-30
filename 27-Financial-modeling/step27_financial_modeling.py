"""
Step 27: Financial Modeling (QUBO)
Solving financial optimization with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def risk_return_qubo(assets, returns, risks, max_risk):
    """
    QUBO for risk-return optimization
    
    assets: list of asset names
    returns: dict of asset -> expected return
    risks: dict of asset -> risk (variance)
    max_risk: maximum acceptable risk
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    return_penalty = 10
    risk_penalty = 20
    
    for asset in assets:
        linear[asset] = -returns.get(asset, 0) * return_penalty
    
    for asset in assets:
        quadratic[(asset, asset)] = risks.get(asset, 0) * risk_penalty
    
    for i, a1 in enumerate(assets):
        for j, a2 in enumerate(assets):
            if i < j:
                cov = risks.get(a1, 0) * risks.get(a2, 0) * 0.5
                quadratic[(a1, a2)] = risk_penalty * 2 * cov
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, assets


def solve_financial(assets, returns, risks, max_risk):
    """Solve financial optimization"""
    
    print("=" * 60)
    print("Step 27: Financial Modeling (QUBO)")
    print("=" * 60)
    
    print(f"\nAssets: {assets}")
    print(f"Returns: {returns}")
    print(f"Risks: {risks}")
    print(f"Max risk: {max_risk}")
    
    bqm, assets = risk_return_qubo(assets, returns, risks, max_risk)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1000, temp=10.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    selected = [a for a in assets if best_state.get(a, 0) == 1]
    print(f"Selected: {selected}")
    
    total_return = sum(returns.get(a, 0) for a in selected)
    total_risk = sum(risks.get(a, 0) for a in selected)
    
    print(f"Total return: {total_return}")
    print(f"Total risk: {total_risk}")
    
    return best_state, best_cost, selected, total_return


def simple_portfolio():
    """Simple portfolio"""
    
    print("\n1. Simple Portfolio")
    print("-" * 40)
    
    assets = ['stock', 'bond', 'gold']
    returns = {'stock': 15, 'bond': 5, 'gold': 8}
    risks = {'stock': 20, 'bond': 5, 'gold': 12}
    max_risk = 25
    
    return solve_financial(assets, returns, risks, max_risk)


def diversified_finance():
    """Diversified financial portfolio"""
    
    print("\n2. Diversified Portfolio")
    print("-" * 40)
    
    assets = ['tech', 'health', 'energy', 'finance', 'utilities']
    returns = {'tech': 20, 'health': 12, 'energy': 15, 'finance': 10, 'utilities': 6}
    risks = {'tech': 25, 'health': 10, 'energy': 18, 'finance': 12, 'utilities': 5}
    max_risk = 30
    
    return solve_financial(assets, returns, risks, max_risk)


if __name__ == "__main__":
    simple_portfolio()
    diversified_finance()