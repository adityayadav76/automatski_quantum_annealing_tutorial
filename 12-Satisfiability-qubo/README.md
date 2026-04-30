# Satisfiability Problems (QUBO)

## Overview
SAT problems ask whether there exists an assignment satisfying a Boolean formula. We convert SAT to QUBO by encoding each clause.

## QUBO Formulation
- For each variable x_i, create binary variable
- For clause (x OR y OR z), add penalty when all literals are false
- Use penalty methods to enforce clause satisfaction

## Running the Example
```bash
python step12_satisfiability.py
```

## Source Code
See `step12_satisfiability.py` for complete implementation.