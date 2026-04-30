# Introduction to QUBO

## Overview
This step introduces the fundamental concept of Quadratic Unconstrained Binary Optimization (QUBO). QUBO is a mathematical optimization problem where we minimize a quadratic function of binary (0/1) variables.

## What is QUBO?
A QUBO problem is defined as:

```
minimize: Σᵢ Qᵢᵢxᵢ + Σᵢ<j Qᵢⱼxᵢxⱼ
subject to: xᵢ ∈ {0, 1}
```

Where:
- xᵢ are binary decision variables (0 or 1)
- Qᵢᵢ are linear coefficients (diagonal elements)
- Qᵢⱼ are quadratic coefficients (off-diagonal elements)

## Why QUBO?
- Universal representation for many optimization problems
- Natural fit for quantum annealers
- Can encode NP-hard problems

## Simple Example
Let's solve a simple QUBO to find the minimum of: x + y - xy where x, y ∈ {0, 1}

The possible solutions are:
- (0,0): 0 + 0 - 0 = 0
- (0,1): 0 + 1 - 0 = 1
- (1,0): 1 + 0 - 0 = 1
- (1,1): 1 + 1 - 1 = 1

Minimum is 0 at (0,0).

## Running the Example
```bash
python step1_intro_qubo.py
```

## Source Code
See `step1_intro_qubo.py` for the complete implementation using Dimod and AutomatskiInitium solver.