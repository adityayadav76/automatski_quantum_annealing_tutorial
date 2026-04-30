# Clustering (QUBO)

## Overview
Clustering groups similar data points together. We formulate it as QUBO by defining which cluster each point belongs to.

## QUBO Formulation
- Variables x_{i,c} = 1 if point i is in cluster c
- One-hot constraint for each point
- Minimize intra-cluster distances

## Running the Example
```bash
python step13_clustering.py
```

## Source Code
See `step13_clustering.py` for complete implementation.