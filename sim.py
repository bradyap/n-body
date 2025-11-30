import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors
import tkinter as tk
from tkinter import ttk
from pathlib import Path

import nbody

SIM_OPTIONS_PATH = Path(__file__).resolve().parent / "sims"
DEFAULT_FNAME = "test_bodies.csv"

DEFAULT_G = 0.001
DEFAULT_DT = 0.001
DEFAULT_THREADS = 1
COMPUTE_MODES = {
    "Serial": nbody.compute_forces_serial,
    "Threaded": nbody.compute_forces_threaded,
    "OpenMP": nbody.compute_forces_omp,
}

AXIS_MIN, AXIS_MAX = -400.0, 400.0
SIZE_MIN, SIZE_MAX = 20, 200
FRAMES_BETWEEN_UPDATES = 100

def prompt_run_config():
    csv_paths = sorted(SIM_OPTIONS_PATH.glob("*.csv"))
    root = tk.Tk()
    root.title("N-Body Simulation")
    root.configure(padx=16, pady=16)

    # get selected options from gui
    mode_var = tk.StringVar(value="Serial")
    file_var = tk.StringVar(value=(SIM_OPTIONS_PATH / DEFAULT_FNAME).name)
    threads_var = tk.IntVar(value=DEFAULT_THREADS)
    g_var = tk.DoubleVar(value=DEFAULT_G)
    dt_var = tk.DoubleVar(value=DEFAULT_DT)
    result = {}

    def submit():
        result.update(
            mode = mode_var.get(),
            file = str(SIM_OPTIONS_PATH / file_var.get()),
            threads = threads_var.get(),
            G = g_var.get(),
            DT = dt_var.get(),
        )
        root.destroy()

    def cancel():
        root.destroy()

    ttk.Label(root, text="Compute mode").grid(row=0, column=0, sticky="w")
    ttk.Combobox(root, textvariable=mode_var, values=list(COMPUTE_MODES.keys()), state="readonly").grid(row=0, column=1, sticky="ew")

    ttk.Label(root, text="Simulation CSV").grid(row=1, column=0, sticky="w")
    ttk.Combobox(root, textvariable=file_var, values=[p.name for p in csv_paths], state="readonly").grid(row=1, column=1, sticky="ew")

    ttk.Label(root, text="Threads").grid(row=2, column=0, sticky="w")
    ttk.Spinbox(root, from_=1, to=128, textvariable=threads_var).grid(row=2, column=1, sticky="ew")

    ttk.Label(root, text="G").grid(row=3, column=0, sticky="w")
    ttk.Entry(root, textvariable=g_var).grid(row=3, column=1, sticky="ew")

    ttk.Label(root, text="DT").grid(row=4, column=0, sticky="w")
    ttk.Entry(root, textvariable=dt_var).grid(row=4, column=1, sticky="ew")

    btn_frame = ttk.Frame(root)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=(12, 0))
    ttk.Button(btn_frame, text="Start", command=submit).pack(side="left", padx=(0, 8))
    ttk.Button(btn_frame, text="Cancel", command=cancel).pack(side="left")

    root.columnconfigure(1, weight=1)
    root.mainloop()
    return result

def print_bodies(bodies_container, N):
    for i in range(N):
        b = bodies_container.get_body(i)
        print(f"Body %d with mass %.3f: Pos(%.3f, %.3f, %.3f) Vel(%.3f, %.3f, %.3f)" % (
            i, b.m, b.x, b.y, b.z, b.vx, b.vy, b.vz))
    print()

def run_sim(bodies, N, calc_func, threads, dt, grav_const):
    # Plot setup
    plt.ion()
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(111, projection='3d')

    mass_values = np.array([bodies.get_body(i).m for i in range(N)], dtype=np.float64)
    log_masses = np.log10(mass_values) # Log scale for better size distribution
    # Scale sizes between set min and max
    mass_norm = (log_masses - log_masses.min()) / (log_masses.max() - log_masses.min())
    marker_sizes = SIZE_MIN + (SIZE_MAX - SIZE_MIN) * mass_norm
    cmap = plt.cm.plasma # Color map to colorize based on mass
    
    def style_axes():
        ax.set_box_aspect([AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN, AXIS_MAX - AXIS_MIN])
        ax.set_xlim(AXIS_MIN, AXIS_MAX)
        ax.set_ylim(AXIS_MIN, AXIS_MAX)
        ax.set_zlim(AXIS_MIN, AXIS_MAX)
        ax.set_facecolor('black')
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Z', color='white')
        ax.tick_params(colors='white')
        ax.grid(False)
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.set_facecolor((0, 0, 0, 0))
            pane.set_edgecolor('white')

    style_axes()
    
    # Key handler to quit on "q"
    quit_sim = False
    def on_key(event):
        nonlocal quit_sim
        if event.key.lower() == 'q':
            quit_sim = True
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    print(f"Starting sim with {N} bodies, func ={calc_func.__name__}, threads={threads}, dt={dt}, G={grav_const}")
    print("Press 'q' to quit simulation")
    
    step = 0
    while not quit_sim:
        # Compute forces
        if threads > 1:
            calc_func(bodies, dt, grav_const, threads)
        else:
            calc_func(bodies, dt, grav_const)

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
        step += 1

    plt.ioff()
    plt.show()

    print("Sim complete!")

def main():
    config = prompt_run_config()
    fname = config["file"]
    threads = config["threads"] if config["mode"] != "Serial" else 1
    dt = config["DT"]
    grav_const = config["G"]
    calc_func = COMPUTE_MODES[config["mode"]]

    # Read initial data for each body from csv
    # x, y, z, vx, vy, vz, mass
    initial_data = pd.read_csv(fname).to_numpy(dtype=np.float64)

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
    run_sim(bodies, N, calc_func, threads, dt, grav_const)

if __name__ == '__main__':
    main()
