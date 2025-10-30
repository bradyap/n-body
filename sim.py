import numpy as np
import pandas as pd
from ctypes import CDLL, c_int, c_double
from numpy.ctypeslib import ndpointer

# Read initial data for each body from csv
# mass, x, y, z, vx, vy, vz
initial_data = pd.read_csv('test_bodies.csv').to_numpy(dtype=np.float64)

# Split data and flatten position/velocity arrays
mass = np.ascontiguousarray(initial_data[:, 0])
pos = np.ascontiguousarray(initial_data[:, 1:4].ravel())
vel = np.ascontiguousarray(initial_data[:, 4:7].ravel())
N = len(mass) # Number of bodies

print(f"Loaded {N} bodies from csv")

# Load shared library
lib = CDLL("./libnbody.so")

lib.step.argtypes = [ # Args for step function
    ndpointer(dtype=np.float64, ndim=1, flags="C_CONTIGUOUS"),  # mass
    ndpointer(dtype=np.float64, ndim=1, flags="C_CONTIGUOUS"),  # pos
    ndpointer(dtype=np.float64, ndim=1, flags="C_CONTIGUOUS"),  # vel
    c_int, # n
    c_double, # dt
    c_double # G
]

# Sim parameters
G = 1; # Gravitational constant, 6.674e-11 in real life
dt = 1; # Time step in seconds
steps = 20 # Number of steps to simulate

# Initial state printout
print("Initial state")
for i in range(N):
        print(f"Body %d with mass %.3f: Pos(%.3f, %.3f, %.3f) Vel(%.3f, %.3f, %.3f)" % (i, mass[i], pos[3*i], pos[3*i+1], pos[3*i+2], vel[3*i], vel[3*i+1], vel[3*i+2]))
print()

for step in range(steps):
    lib.step(mass, pos, vel, N, dt, G) # Call c++ code to update 

    # Print updated positions and velocities
    print(f"Step " + str(step + 1))
    for i in range(N):
        print(f"Body %d with mass %.3f: Pos(%.3f, %.3f, %.3f) Vel(%.3f, %.3f, %.3f)" % (i, mass[i], pos[3*i], pos[3*i+1], pos[3*i+2], vel[3*i], vel[3*i+1], vel[3*i+2]))
    print()
    
    # Visualize here

print("Sim complete")