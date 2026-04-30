"""
Step 16: Job Scheduling (QUBO)
Solving job scheduling with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def job_scheduling_qubo(jobs, precedence, time_slots):
    """
    Create QUBO for job scheduling
    
    jobs: list of job names
    precedence: list of (job_i, job_j) meaning i before j
    time_slots: number of available time slots
    """
    
    n = len(jobs)
    t = time_slots
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 50
    precedence_penalty = 30
    
    for j, job in enumerate(jobs):
        for time in range(t):
            linear[(job, time)] = 0
    
    for j, job in enumerate(jobs):
        for t1 in range(t):
            for t2 in range(t1 + 1, t):
                var1 = (job, t1)
                var2 = (job, t2)
                quadratic[(var1, var2)] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    for time in range(t):
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                var1 = (jobs[j1], time)
                var2 = (jobs[j2], time)
                quadratic[(var1, var2)] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    for (job_i, job_j) in precedence:
        for t_i in range(t):
            for t_j in range(t_i + 1, t):
                var_i = (job_i, t_i)
                var_j = (job_j, t_j)
                if var_i in [v for v in quadratic]:
                    quadratic[var_i] = quadratic.get(var_i, 0) + precedence_penalty
                else:
                    quadratic[var_i] = precedence_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, jobs


def solve_job_scheduling(jobs, precedence, time_slots):
    """Solve job scheduling"""
    
    print("=" * 60)
    print("Step 16: Job Scheduling (QUBO)")
    print("=" * 60)
    
    print(f"\nJobs: {jobs}")
    print(f"Precedence: {precedence}")
    print(f"Time slots: {time_slots}")
    
    bqm, jobs = job_scheduling_qubo(jobs, precedence, time_slots)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1500, temp=12.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution: {best_state}")
    print(f"Energy: {best_cost}")
    
    schedule = {}
    for job in jobs:
        for time in range(time_slots):
            if best_state.get((job, time), 0) == 1:
                schedule[job] = time
    
    print(f"Schedule: {schedule}")
    
    valid = True
    for job_i, job_j in precedence:
        if job_i in schedule and job_j in schedule:
            if schedule[job_i] >= schedule[job_j]:
                print(f"Precedence violated: {job_i} after {job_j}")
                valid = False
    
    print(f"Valid schedule: {valid}")
    
    return best_state, best_cost, schedule, valid


def simple_schedule():
    """Simple job scheduling"""
    
    print("\n1. Simple Job Scheduling")
    print("-" * 40)
    
    jobs = ['A', 'B', 'C']
    precedence = [('A', 'B'), ('B', 'C')]
    time_slots = 3
    
    return solve_job_scheduling(jobs, precedence, time_slots)


def parallel_jobs():
    """Schedule with parallel jobs"""
    
    print("\n2. Parallel Jobs")
    print("-" * 40)
    
    jobs = ['J1', 'J2', 'J3', 'J4']
    precedence = [('J1', 'J3'), ('J2', 'J3')]
    time_slots = 3
    
    return solve_job_scheduling(jobs, precedence, time_slots)


def complex_precedence():
    """Complex precedence constraints"""
    
    print("\n3. Complex Precedence")
    print("-" * 40)
    
    jobs = ['design', 'implement', 'test', 'deploy', 'maintain']
    precedence = [
        ('design', 'implement'),
        ('design', 'test'),
        ('implement', 'test'),
        ('test', 'deploy'),
        ('deploy', 'maintain')
    ]
    time_slots = 5
    
    return solve_job_scheduling(jobs, precedence, time_slots)


def project_schedule():
    """Software project scheduling"""
    
    print("\n4. Software Project Schedule")
    print("-" * 40)
    
    jobs = ['req', 'design', 'code', 'test', 'deploy']
    precedence = [
        ('req', 'design'),
        ('design', 'code'),
        ('code', 'test'),
        ('test', 'deploy')
    ]
    time_slots = 5
    
    return solve_job_scheduling(jobs, precedence, time_slots)


if __name__ == "__main__":
    simple_schedule()
    parallel_jobs()
    complex_precedence()
    project_schedule()