# Setting up Dimod

## Overview
This step covers how to set up and configure the Dimod library for working with QUBO problems. Dimod is a Python library for working with binary quadratic models.

## Installation
```bash
pip install dimod
```

Or use the provided requirements.txt:
```bash
pip install -r requirements.txt
```

## Key Concepts
- **BinaryQuadraticModel (BQM)**: The core data structure in Dimod
- **Variable types**: BINARY (0 or 1) and SPIN (-1 or +1)
- **Linear terms**: Coefficients for single variables
- **Quadratic terms**: Coefficients for interaction between variables

## Creating a BQM
```python
import dimod

linear = {'x': 1.0, 'y': 2.0}
quadratic = {('x', 'y'): -1.0}
offset = 0.0

bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
```

## Running the Example
```bash
python step2_setup_dimod.py
```

## Source Code
See `step2_setup_dimod.py` for complete implementation with examples.