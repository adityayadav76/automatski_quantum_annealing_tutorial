"""
Step 18: Image Segmentation (QUBO)
Solving image segmentation with QUBO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dimod

from AutomatskiInitium import AutomatskiInitiumSASolver

HOST = "168.220.234.162"
PORT = 80


def image_segmentation_qubo(pixels, num_segments):
    """
    Create QUBO for image segmentation
    
    pixels: list of (intensity, x, y) tuples
    num_segments: number of segments
    """
    
    n = len(pixels)
    
    linear = {}
    quadratic = {}
    offset = 0
    
    one_hot_penalty = 50
    similarity_penalty = 10
    
    for i in range(n):
        for s in range(num_segments):
            linear[(i, s)] = 0
    
    for i in range(n):
        for s1 in range(num_segments):
            for s2 in range(s1 + 1, num_segments):
                var1 = (i, s1)
                var2 = (i, s2)
                quadratic[(var1, var2)] = one_hot_penalty * 2
        offset += one_hot_penalty
    
    for i in range(n):
        for j in range(i + 1, n):
            intensity_i = pixels[i][0]
            intensity_j = pixels[j][0]
            diff = abs(intensity_i - intensity_j)
            
            for s in range(num_segments):
                var_i = (i, s)
                var_j = (j, s)
                quadratic[(var_i, var_j)] = quadratic.get((var_i, var_j), 0) + similarity_penalty * diff
    
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype=dimod.BINARY)
    
    return bqm, n


def solve_image_segmentation(pixels, num_segments):
    """Solve image segmentation"""
    
    print("=" * 60)
    print("Step 18: Image Segmentation (QUBO)")
    print("=" * 60)
    
    print(f"\nNumber of pixels: {len(pixels)}")
    print(f"Segments: {num_segments}")
    
    bqm, n = image_segmentation_qubo(pixels, num_segments)
    
    solver = AutomatskiInitiumSASolver(host=HOST, port=PORT, max_iter=1500, temp=12.0, cooling_rate=0.01, num_reads=10)
    
    qubo, offset_val = bqm.to_qubo()
    best_state, best_cost = solver.solve(qubo)
    best_cost = best_cost + offset_val
    
    print(f"\nSolution (first 10 assignments): {dict(list(best_state.items())[:10])}")
    print(f"Energy: {best_cost}")
    
    segments = {s: [] for s in range(num_segments)}
    for i in range(n):
        for s in range(num_segments):
            if best_state.get((i, s), 0) == 1:
                segments[s].append(i)
                break
    
    print(f"Segments: {segments}")
    
    for s in range(num_segments):
        if segments[s]:
            avg_intensity = sum(pixels[i][0] for i in segments[s]) / len(segments[s])
            print(f"Segment {s}: {len(segments[s])} pixels, avg intensity: {avg_intensity:.2f}")
    
    return best_state, best_cost, segments


def two_tone_image():
    """Simple two-tone image"""
    
    print("\n1. Two-Tone Image")
    print("-" * 40)
    
    pixels = [
        (10, 0, 0), (10, 1, 0), (10, 2, 0),
        (90, 0, 1), (90, 1, 1), (90, 2, 1),
        (10, 0, 2), (10, 1, 2), (10, 2, 2)
    ]
    num_segments = 2
    
    return solve_image_segmentation(pixels, num_segments)


def grayscale_gradient():
    """Grayscale gradient image"""
    
    print("\n2. Grayscale Gradient")
    print("-" * 40)
    
    pixels = []
    for y in range(3):
        for x in range(3):
            intensity = (x + y) * 30 + 10
            pixels.append((intensity, x, y))
    
    num_segments = 3
    
    return solve_image_segmentation(pixels, num_segments)


def four_region_image():
    """Four distinct regions"""
    
    print("\n3. Four Region Image")
    print("-" * 40)
    
    pixels = [
        (10, 0, 0), (10, 0, 1), (20, 0, 2),
        (20, 1, 0), (20, 1, 1), (20, 1, 2),
        (80, 2, 0), (80, 2, 1), (90, 2, 2),
        (90, 3, 0), (90, 3, 1), (90, 3, 2)
    ]
    num_segments = 4
    
    return solve_image_segmentation(pixels, num_segments)


def noisy_image():
    """Noisy image with clear pattern"""
    
    print("\n4. Noisy Image with Pattern")
    print("-" * 40)
    
    pixels = [
        (50, 0, 0), (55, 0, 1), (100, 0, 2),
        (45, 1, 0), (50, 1, 1), (95, 1, 2),
        (100, 2, 0), (105, 2, 1), (150, 2, 2)
    ]
    num_segments = 2
    
    return solve_image_segmentation(pixels, num_segments)


if __name__ == "__main__":
    two_tone_image()
    grayscale_gradient()
    four_region_image()
    noisy_image()