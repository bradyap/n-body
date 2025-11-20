import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

# Visualization config
AXIS_MIN, AXIS_MAX = -200.0, 200.0 # Axis size of plot
FRAMES_BETWEEN_UPDATES = 250 # How many sim steps between plot updates 

def main():
    df = pd.read_csv("nbody_locations.csv")
    grouped = df.groupby("step")

    all_positions = []
    for step, group in grouped:
        xs = group["x"].values
        ys = group["y"].values
        zs = group["z"].values
        all_positions.append((xs, ys, zs))

    print(f"Loaded {len(all_positions)} frames")


# ---------------- Setup plot ----------------
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_box_aspect([AXIS_MAX - AXIS_MIN]*3)
    ax.set_xlim(AXIS_MIN, AXIS_MAX)
    ax.set_ylim(AXIS_MIN, AXIS_MAX)
    ax.set_zlim(AXIS_MIN, AXIS_MAX)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Initialize scatter with first frame
    xs, ys, zs = all_positions[0]
    scatter = ax.scatter(xs, ys, zs, s=2)

    # ---------------- Animating Plot ----------------
    print("\nAnimating...")
    def update(frame):
        xs, ys, zs = all_positions[frame]
        scatter._offsets3d = (xs, ys, zs)
        ax.set_title(f"Step {frame*FRAMES_BETWEEN_UPDATES}")  # Optional title
        return scatter,
    
    ani = FuncAnimation(
        fig, 
        update, 
        frames=len(all_positions), 
        interval=25,  # milliseconds between frames
        blit=False    # Must be False for 3D scatter plots
    )

    plt.show()
    print("Simulation Complete")
    return ani


if __name__ == '__main__':
    ani = main()