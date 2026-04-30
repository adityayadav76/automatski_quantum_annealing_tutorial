"""
Step 21: Time Tabling (QUBO)
Solving university timetabling with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def timetabling_qubo(courses, time_slots, rooms):
    """
    Create QUBO for timetabling
    
    courses: list of course names
    time_slots: list of time slots
    rooms: list of rooms
    """
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 50
    conflict_penalty = 30
    
    for course in courses:
        for time in time_slots:
            for room in rooms:
                linear[(course, time, room)] = 0
    
    for course in courses:
        for time in time_slots:
            for r1 in range(len(rooms)):
                for r2 in range(r1 + 1, len(rooms)):
                    var1 = (course, time, rooms[r1])
                    var2 = (course, time, rooms[r2])
                    quadratic[(var1, var2)] = one_hot_penalty * 2
            offset += one_hot_penalty
    
    for time in time_slots:
        for room in rooms:
            for c1 in range(len(courses)):
                for c2 in range(c1 + 1, len(courses)):
                    var1 = (courses[c1], time, room)
                    var2 = (courses[c2], time, room)
                    quadratic[(var1, var2)] = conflict_penalty * 2
            offset += conflict_penalty
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, courses, time_slots, rooms


def solve_timetabling(courses, time_slots, rooms):
    """Solve timetabling"""
    
    print("=" * 60)
    print("Step 21: Time Tabling (QUBO)")
    print("=" * 60)
    
    print(f"\nCourses: {courses}")
    print(f"Time slots: {time_slots}")
    print(f"Rooms: {rooms}")
    
    bqm, courses, time_slots, rooms = timetabling_qubo(courses, time_slots, rooms)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1500, temp=12.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution (first 5): {dict(list(best_state.items())[:5])}")
    print(f"Energy: {best_cost}")
    
    schedule = {}
    for course in courses:
        for time in time_slots:
            for room in rooms:
                if best_state.get((course, time, room), 0) == 1:
                    schedule[course] = (time, room)
    
    print(f"Schedule: {schedule}")
    
    return best_state, best_cost, schedule


def simple_timetable():
    """Simple timetabling"""
    
    print("\n1. Simple Timetable")
    print("-" * 40)
    
    courses = ['Math', 'Physics', 'Chem']
    time_slots = ['Mon-AM', 'Mon-PM', 'Tue-AM']
    rooms = ['R1', 'R2']
    
    return solve_timetabling(courses, time_slots, rooms)


def course_timetable():
    """University course scheduling"""
    
    print("\n2. University Course Timetable")
    print("-" * 40)
    
    courses = ['CS101', 'CS201', 'MATH101', 'PHY101']
    time_slots = ['Mon-AM', 'Mon-PM', 'Tue-AM', 'Tue-PM', 'Wed-AM']
    rooms = ['R1', 'R2', 'R3']
    
    return solve_timetabling(courses, time_slots, rooms)


def larger_timetable():
    """Larger timetable"""
    
    print("\n3. Larger Timetable")
    print("-" * 40)
    
    courses = ['A', 'B', 'C', 'D', 'E']
    time_slots = ['T1', 'T2', 'T3', 'T4']
    rooms = ['R1', 'R2']
    
    return solve_timetabling(courses, time_slots, rooms)


if __name__ == "__main__":
    simple_timetable()
    course_timetable()
    larger_timetable()