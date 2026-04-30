# Traveling Salesman Problem (QUBO)

## Overview
TSP finds the shortest Hamiltonian cycle visiting all cities exactly once. We encode it as QUBO using binary variables x_{i,t} = 1 if city i is visited at time t.

## QUBO Formulation
- Each city assigned a position in the tour
- One-hot constraints for cities and positions
- Adjacency constraints to ensure valid tours

## Running the Example
```bash
python step11_tsp.py
```

## Source Code
See `step11_tsp.py` for complete implementation.