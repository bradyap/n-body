import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import time

import nbody_OpenMP

# Input file name
FNAME = "test_bodies1000.csv"

# Sim parameters
#G = 6.674e-11 # Gravitational constant
G = 0.001 # for testing
DT = 0.001 # Time step in seconds
NUM_STEPS = 100000 # Number of steps to simulate

# Visualization config
AXIS_MIN, AXIS_MAX = -200.0, 200.0 # Axis size of plot
FRAMES_BETWEEN_UPDATES = 250 # How many sim steps between plot updates

def print_bodies(bodies_container, N):
    for i in range(N):
        b = bodies_container.get_body(i)
        print(f"Body %d with mass %.3f: Pos(%.3f, %.3f, %.3f) Vel(%.3f, %.3f, %.3f)" % (i, b.m, b.x, b.y, b.z, b.vx, b.vy, b.vz))
    print()


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
def percentage_bar(current, total, start_time,bar_length=30):
    percent = (current + 1) / total
    filled_length = int(bar_length * percent)
    bar = f"{GREEN}{'█' * filled_length}{RED}{' ' * (bar_length - filled_length)}{RESET}"
    now = time.time()
    elapsed = now - start_time

    # Avoid division by zero
    if current == 0:
        eta = 0
    else:
        steps_per_sec = current / elapsed
        remaining = total - current
        eta = remaining / steps_per_sec

    # Format ETA as h:m:s
    eta_h = int(eta // 3600)
    eta_m = int((eta % 3600) // 60)
    eta_s = int(eta % 60)
    eta_str = f"{eta_h:02d}:{eta_m:02d}:{eta_s:02d}"

    print(f"\r|{bar}| {percent*100:5.1f}%  ETA: {eta_str}", end="")



def main():
    # Read initial data for each body from csv
    # x, y, z, vx, vy, vz, mass
    initial_data = pd.read_csv(FNAME).to_numpy(dtype=np.float64)
    times = []

    # Split data
    pos = initial_data[:, 0:3]
    vel = initial_data[:, 3:6]
    mass = initial_data[:, 6]
    N = len(mass)  # Number of bodies

    print(f"Loaded {N} bodies from csv")

    # Create bodies container
    bodies = nbody_OpenMP.BodiesContainer(N)
    
    # Initialize bodies
    bodies.set_all(pos[:,0], pos[:,1], pos[:,2], vel[:,0], vel[:,1], vel[:,2], mass)

    # ---------------- Precomputing Positions ----------------

    print("Precomputing positions...")
    start_time = time.time()
    all_positions = []  # list of tuples (xs, ys, zs)
    for step in range(NUM_STEPS):
        nbody_OpenMP.compute_forces_OpenMP(bodies, DT, G, 16)

        if step % FRAMES_BETWEEN_UPDATES == 0:
            xs = [bodies.get_body(i).x for i in range(N)]
            ys = [bodies.get_body(i).y for i in range(N)]
            zs = [bodies.get_body(i).z for i in range(N)]
            all_positions.append((xs, ys, zs))
            percentage_bar(step, NUM_STEPS, start_time)

    print(f"\nPrecomputation complete: {len(all_positions)} frames")

    rows = []

    for step_idx, (xs, ys, zs) in enumerate(all_positions):
        for i in range(N):
            rows.append([step_idx * FRAMES_BETWEEN_UPDATES, i, xs[i], ys[i], zs[i]])

    df = pd.DataFrame(rows, columns=["step", "body", "x", "y", "z"])
    df.to_csv("nbody_locations.csv", index=False)

if __name__ == '__main__':
    main()



