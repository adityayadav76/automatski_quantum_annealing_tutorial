# Knapsack Problem

## Overview
The knapsack problem is a classic optimization problem: given a set of items with weights and values, maximize total value while staying within weight capacity.

## QUBO Formulation
- Binary variable x_i = 1 if item i is selected
- Objective: maximize Σ value_i * x_i
- Constraint: Σ weight_i * x_i ≤ capacity
- Use penalty method for constraint

## Running the Example
```bash
python step8_knapsack.py
```

## Source Code
See `step8_knapsack.py` for complete implementation.