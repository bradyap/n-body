import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import nbody

# Input file name
FNAME = "test_bodies300.csv"

# Sim parameters
# G = 6.674e-11 # Gravitational constant
G = 0.001  # for testing
DT = 0.001  # Time step in seconds
NUM_STEPS = 1000000000  # Number of steps to simulate

# Visualization config
AXIS_MIN, AXIS_MAX = -400.0, 400.0  # Axis size of plot
FRAMES_BETWEEN_UPDATES = 100  # How many sim steps between plot updates

def print_bodies(bodies_container, N):
    for i in range(N):
        b = bodies_container.get_body(i)
        print(f"Body %d with mass %.3f: Pos(%.3f, %.3f, %.3f) Vel(%.3f, %.3f, %.3f)" % (
            i, b.m, b.x, b.y, b.z, b.vx, b.vy, b.vz))
    print()

def main():
    # Read initial data for each body from csv
    # x, y, z, vx, vy, vz, mass
    initial_data = pd.read_csv(FNAME).to_numpy(dtype=np.float64)

    # Split data
    pos = initial_data[:, 0:3]
    vel = initial_data[:, 3:6]
    mass = initial_data[:, 6]
    N = len(mass)  # Number of bodies

    print(f"Loaded {N} bodies from csv")

    # Create bodies container
    bodies = nbody.BodiesContainer(N)

    # Initialize bodies
    bodies.set_all(pos[:, 0], pos[:, 1], pos[:, 2], vel[:, 0], vel[:, 1], vel[:, 2], mass)

    # Initial state printout
    print("Initial state")
    print_bodies(bodies, N)

    # Plot setup
    plt.ion()
    # Make figure bigger (width, height in inches)
    fig = plt.figure(figsize=(12, 10))
    fig.patch.set_facecolor('black')  # Set figure background to black
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')  # Set axes background to black

    # Lock the box aspect so distances look right
    ax.set_box_aspect([AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN])
    ax.set_xlim(AXIS_MIN, AXIS_MAX)
    ax.set_ylim(AXIS_MIN, AXIS_MAX)
    ax.set_zlim(AXIS_MIN, AXIS_MAX)
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z', color='white')

    # Make axis lines and tick labels white
    ax.tick_params(colors='white')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.yaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.set_edgecolor('white')
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

    for step in range(NUM_STEPS):
        # nbody.compute_forces_serial(bodies, DT, G)
        # nbody.compute_forces_threaded(bodies, DT, G, 16)
        nbody.compute_forces_omp(bodies, DT, G, 32)

        # Print updated positions and velocities
        # print(f"Step " + str(step + 1))
        # print_bodies(bodies, N)

        if (step + 1) % FRAMES_BETWEEN_UPDATES == 0:
            ax.clear()
            ax.set_facecolor('black')  # Reset background after clear

            xs = [bodies.get_body(i).x for i in range(N)]
            ys = [bodies.get_body(i).y for i in range(N)]
            zs = [bodies.get_body(i).z for i in range(N)]
            masses = [bodies.get_body(i).m for i in range(N)]

            # Scale sizes for better visibility
            sizes = [np.sqrt(m) * 1.5 for m in masses]
            
            ax.scatter(xs, ys, zs, s=sizes, c='white', alpha=0.8)

            # re-apply fixed limits and labels after clear()
            ax.set_box_aspect(
                [AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN])
            ax.set_xlim(AXIS_MIN, AXIS_MAX)
            ax.set_ylim(AXIS_MIN, AXIS_MAX)
            ax.set_zlim(AXIS_MIN, AXIS_MAX)
            ax.set_xlabel('X', color='white')
            ax.set_ylabel('Y', color='white')
            ax.set_zlabel('Z', color='white')

            # Reapply white styling after clear
            ax.tick_params(colors='white')
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor('white')
            ax.yaxis.pane.set_edgecolor('white')
            ax.zaxis.pane.set_edgecolor('white')
            ax.grid(color='gray', linestyle='--', linewidth=0.5)

            plt.draw()
            plt.pause(0.001)

    # Keep the last plot open
    plt.ioff()
    plt.show()

    print("sim complete")

if __name__ == '__main__':
    main()
