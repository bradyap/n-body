import numpy as np
import pandas as pd

import nbody

# Sim parameters
G = 6.674e-11 # Gravitational constant
#G = 1.0
DT = 100000.0 # Time step in seconds
NUM_STEPS = 20 # Number of steps to simulate


def print_bodies(bodies_container, N):
    for i in range(N):
        b = bodies_container.get_body(i)
        print(f"Body %d with mass %.3f: Pos(%.3f, %.3f, %.3f) Vel(%.3f, %.3f, %.3f)" % (i, b.m, b.x, b.y, b.z, b.vx, b.vy, b.vz))
    print()


def main():
    # Read initial data for each body from csv
    # x, y, z, vx, vy, vz, mass
    initial_data = pd.read_csv('test_bodies.csv').to_numpy(dtype=np.float64)

    # Split data
    pos = initial_data[:, 0:3]
    vel = initial_data[:, 3:6]
    mass = initial_data[:, 6]
    N = len(mass)  # Number of bodies

    print(f"Loaded {N} bodies from csv")

    # Create bodies container
    bodies = nbody.BodiesContainer(N)
    
    # Initialize bodies
    for i in range(N):
        bodies.set_body(i, pos[i,0], pos[i,1], pos[i,2], vel[i,0], vel[i,1], vel[i,2], mass[i])

    # Initial state printout
    print("Initial state")
    print_bodies(bodies, N)
    
    for step in range(NUM_STEPS):
        nbody.compute_forces_serial(bodies, DT, G)

        # Print updated positions and velocities
        print(f"Step " + str(step + 1))
        print_bodies(bodies, N)

        # Visualize here

    print("sim complete")

if __name__ == '__main__':
    main()



