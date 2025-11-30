import numpy as np
import pandas as pd

# -----------------------------
# Galaxy generation parameters
# -----------------------------
N = 200            # number of bodies
R_MAX = 350        # max radius of galaxy disk
G = 0.001          # gravitational constant used in simulation
VELOCITY_SCALE = 4.0   # increase orbital speed so visualization moves nicely

# -----------------------------
# Generate galaxy-like positions
# -----------------------------
# random radius distribution biased toward center
r = np.sqrt(np.random.uniform(0, R_MAX**2, N))  

# random angle
theta = np.random.uniform(0, 2*np.pi, N)

# convert to Cartesian
x = r * np.cos(theta)
y = r * np.sin(theta)
z = np.zeros(N)     # keep in 2D plane for stability

# -----------------------------
# Generate masses
# -----------------------------
mass = np.random.uniform(0.5, 5.0, N)  # small mass range for stable galaxy

# -----------------------------
# Generate orbital velocities
# -----------------------------
# circular orbit speed formula, scaled up
v_circ = VELOCITY_SCALE * np.sqrt(G * mass / (r + 1e-6))

# tangential direction
vx = -v_circ * np.sin(theta)
vy =  v_circ * np.cos(theta)
vz = np.zeros(N)  # stay in plane

# -----------------------------
# Export to CSV
# -----------------------------
df = pd.DataFrame({
    "x": x,
    "y": y,
    "z": z,
    "vx": vx,
    "vy": vy,
    "vz": vz,
    "mass": mass
})

df.to_csv("system.csv", index=False)
print("✓ Generated galaxy_200.csv with 200 bodies")
