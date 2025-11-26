import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors

import nbody

# Input file name
FNAME = "test_bodies300.csv"

# Sim parameters
# G = 6.674e-11 # Gravitational constant
G = 0.001  # for testing
DT = 0.001  # Time step in seconds
NUM_STEPS = 1000000000  # Number of steps to simulate

# Visualization config
AXIS_MIN, AXIS_MAX = -200.0, 200.0  # Axis size of plot
FRAMES_BETWEEN_UPDATES = 100  # How many sim steps between plot updates


def print_bodies(bodies_container, N):
    for i in range(N):
        b = bodies_container.get_body(i)
        print(f"Body %d with mass %.3f: Pos(%.3f, %.3f, %.3f) Vel(%.3f, %.3f, %.3f)" % (
            i, b.m, b.x, b.y, b.z, b.vx, b.vy, b.vz))
    print()


def run_sim(bodies, N, calc_func, threads):
    # Plot setup
    plt.ion()
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(111, projection='3d')

    mass_values = np.array(
        [bodies.get_body(i).m for i in range(N)], dtype=np.float64)
    safe_masses = np.clip(mass_values, a_min=1e-12, a_max=None)
    log_masses = np.log10(safe_masses)
    mass_norm = (log_masses - log_masses.min()) / \
        (log_masses.max() - log_masses.min() + 1e-12)
    size_min, size_max = 30, 260
    marker_sizes = size_min + (size_max - size_min) * mass_norm
    cmap = plt.cm.plasma
    norm = colors.Normalize(vmin=log_masses.min(), vmax=log_masses.max())
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])

    colorbar = fig.colorbar(sm, ax=ax, shrink=0.65, pad=0.08)
    colorbar.set_label(r'$\log_{10}(\mathrm{mass})$', color='white')
    colorbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(colorbar.ax.get_yticklabels(), color='white')

    def style_axes():
        ax.set_box_aspect([AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN])
        ax.set_xlim(AXIS_MIN, AXIS_MAX)
        ax.set_ylim(AXIS_MIN, AXIS_MAX)
        ax.set_zlim(AXIS_MIN, AXIS_MAX)
        ax.set_facecolor('black')
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.set_title('N-Body Simulation', color='white', pad=12)
        ax.tick_params(colors='white')
        ax.grid(False)
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.set_facecolor((0, 0, 0, 0))
            pane.set_edgecolor('white')

    style_axes()

    for step in range(NUM_STEPS):
        # Compute forces
        if threads > 1:
            calc_func(bodies, DT, G, threads)
        else:
            calc_func(bodies, DT, G)

        # Print updated positions and velocities
        # print(f"Step " + str(step + 1))
        # print_bodies(bodies, N)

        if (step + 1) % FRAMES_BETWEEN_UPDATES == 0:
            ax.clear()
            style_axes()
            xs = [bodies.get_body(i).x for i in range(N)]
            ys = [bodies.get_body(i).y for i in range(N)]
            zs = [bodies.get_body(i).z for i in range(N)]

            ax.scatter(
                xs, ys, zs,
                s=marker_sizes,
                c=mass_norm,
                cmap=cmap,
                edgecolors='white',
                linewidths=0.25,
                alpha=0.9,
                depthshade=True
            )

            plt.draw()
            plt.pause(0.001)

    plt.ioff()
    plt.show()

    print("sim complete")


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

    # Run simulation
    run_sim(bodies, N, nbody.compute_forces_omp, 32)


if __name__ == '__main__':
    main()
