# Creating Binary Quadratic Models (BQM)

## Overview
This step focuses on creating Binary Quadratic Models using various methods in Dimod. We explore different ways to construct BQMs for QUBO problems.

## Methods for Creating BQM

### 1. Direct Constructor
```python
bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype)
```

### 2. From QUBO Dictionary
```python
Q = {('x', 'x'): 1, ('x', 'y'): -2, ('y', 'y'): 1}
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
```

### 3. From Ising Model
```python
h = {'x': 0.5, 'y': -0.3}
J = {('x', 'y'): 1.0}
bqm = dimod.BinaryQuadraticModel.from_ising(h, J)
```

### 4. Empty BQM and Add Terms
```python
bqm = dimod.BinaryQuadraticModel.empty(dimod.BINARY)
bqm.add_variable('x', 1.0)
bqm.add_interaction('x', 'y', -1.0)
```

## Running the Example
```bash
python step3_creating_bqm.py
```

## Source Code
See `step3_creating_bqm.py` for complete implementation.