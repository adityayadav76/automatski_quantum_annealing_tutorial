# One-Hot Encoding

## Overview
One-hot encoding is a constraint that ensures exactly one variable out of a group is 1 (and the rest are 0). This is crucial for representing discrete choices in QUBO.

## Mathematical Formulation
For n variables, one-hot means: Σᵢ xᵢ = 1

This is enforced using penalty function:
P = λ * Σᵢ<j (xᵢ - xⱼ)² = λ * (n - 2Σᵢ xᵢ + Σᵢ<j xᵢxⱼ)

## Running the Example
```bash
python step7_one_hot.py
```

## Source Code
See `step7_one_hot.py` for complete implementation.