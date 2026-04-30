# Max-Cut Problem

## Overview
Max-Cut aims to partition vertices of a graph into two sets to maximize the number of edges crossing between the sets.

## QUBO Formulation
- Variable x_i ∈ {0,1} represents which partition vertex i belongs to
- Objective: maximize Σ_{(i,j)∈E} (x_i XOR x_j) = Σ_{(i,j)∈E} (x_i + x_j - 2*x_i*x_j)
- Equivalent to minimizing -Σ_{(i,j)∈E} (x_i + x_j - 2*x_i*x_j)

## Running the Example
```bash
python step10_maxcut.py
```

## Source Code
See `step10_maxcut.py` for complete implementation.