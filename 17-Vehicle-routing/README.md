# Vehicle Routing Problem (QUBO)

## Overview
VRP finds optimal routes for vehicles to visit all customers. We use QUBO to encode the vehicle routing problem.

## QUBO Formulation
- Binary variables x_{v,i} = 1 if vehicle v visits customer i in order
- One-hot constraints for customer visits
- Route continuity constraints

## Running the Example
```bash
python step17_vehicle_routing.py
```

## Source Code
See `step17_vehicle_routing.py` for complete implementation.