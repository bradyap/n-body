import numpy as np
import pandas as pd

np.random.seed(42)

# Must match your sim
G = 0.001

num_bodies = 200
num_stars = num_bodies - 1

# Galaxy size
R_max = 280.0        # max disk radius (fits well in +/- 400)
z_sigma = 15.0       # thickness of the disk

# Central "black hole" mass
M_core = 5000.0

# How fast you want it to spin visually
# 1.0 ~ physically reasonable; 1.5–2.0 = faster but still usually bound for a while
demo_speed_factor = 3.0

rows = []

# --- Central massive body at origin ---
rows.append({
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
    "vx": 0.0,
    "vy": 0.0,
    "vz": 0.0,
    "mass": M_core,
})

# --- Stars in a rotating disk ---

# Radii biased toward the center (sqrt gives more density near 0)
u = np.random.rand(num_stars)
r = R_max * np.sqrt(u)

theta = 2.0 * np.pi * np.random.rand(num_stars)
z = np.random.normal(0.0, z_sigma, num_stars)

x = r * np.cos(theta)
y = r * np.sin(theta)

# Stellar masses
m_star = np.random.uniform(0.5, 3.0, num_stars)

# Approx circular speed due to central mass
eps = 1e-3
v_circ = np.sqrt(G * M_core / (r + eps))

# Scale up for a more dynamic demo
v_circ *= demo_speed_factor

# Tangential velocities in the xy plane
vx = -v_circ * np.sin(theta)
vy =  v_circ * np.cos(theta)
vz = np.random.normal(0.0, 0.02 * np.mean(v_circ), num_stars)  # slight vertical motion

# Collect all bodies
all_x = [0.0] + list(x)
all_y = [0.0] + list(y)
all_z = [0.0] + list(z)
all_vx = [0.0] + list(vx)
all_vy = [0.0] + list(vy)
all_vz = [0.0] + list(vz)
all_m  = [M_core] + list(m_star)

# --- Zero out center-of-mass velocity so galaxy doesn't drift ---

total_mass = np.sum(all_m)
px = np.sum(np.array(all_m) * np.array(all_vx))
py = np.sum(np.array(all_m) * np.array(all_vy))
pz = np.sum(np.array(all_m) * np.array(all_vz))

vx_com = px / total_mass
vy_com = py / total_mass
vz_com = pz / total_mass

all_vx = list(np.array(all_vx) - vx_com)
all_vy = list(np.array(all_vy) - vy_com)
all_vz = list(np.array(all_vz) - vz_com)

# --- Build DataFrame and save ---

df = pd.DataFrame({
    "x": all_x,
    "y": all_y,
    "z": all_z,
    "vx": all_vx,
    "vy": all_vy,
    "vz": all_vz,
    "mass": all_m,
})

df.to_csv("galaxy_single_200.csv", index=False)
print("Wrote galaxy_single_200.csv with", len(df), "bodies")