# Graph Coloring

## Overview
Graph coloring assigns colors to vertices such that no adjacent vertices share the same color. This is an NP-hard problem.

## QUBO Formulation
- Variable x_{v,c} = 1 if vertex v gets color c
- One-hot constraint: each vertex gets exactly one color
- Constraint: adjacent vertices can't have same color

## Running the Example
```bash
python step9_graph_coloring.py
```

## Source Code
See `step9_graph_coloring.py` for complete implementation.