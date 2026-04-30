# Job Scheduling (QUBO)

## Overview
Job scheduling assigns jobs to time slots while respecting constraints like precedence and resource limits.

## QUBO Formulation
- Binary variable x_{j,t} = 1 if job j is scheduled at time t
- Precedence constraints: if i before j, then t_i < t_j
- Resource constraints: at most one job per time slot

## Running the Example
```bash
python step16_job_scheduling.py
```

## Source Code
See `step16_job_scheduling.py` for complete implementation.