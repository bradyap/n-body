import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import time
import nbody

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
def percentage_bar(current, total, N, bar_length=30,):
    percent = (current) / total
    filled_length = int(bar_length * percent)
    bar = f"{GREEN}{'█' * filled_length}{RED}{' ' * (bar_length - filled_length)}{RESET}"
    print(f'\r|{bar}| {percent*100:.01f}% Completed  N = {N}', end='')

G = 0.001
DT = 0.001
N_list = [500, 1000, 2000, 4000, 5000]
threads_list = [1,2,4,8,16,32]
repeat = 100

pos_min, pos_max = -50, 50
vel_min, vel_max = -1, 1
mass_min, mass_max = 0.1, 10

times_N = []
times = []

count = 0
for N in N_list:
    bodies = nbody.BodiesContainer(N)

    pos = np.random.uniform(pos_min, pos_max, (N, 3))
    vel = np.random.uniform(vel_min, vel_max, (N, 3))
    mass = np.random.uniform(mass_min, mass_max, N)

    duration = nbody.benchmark_serial(bodies, DT, G, 100)
    count += 1

    percentage_bar(count, int(len(N_list)), N)

    times_N.append(N)
    times.append(duration)

print("")


df = pd.DataFrame({
    "N": times_N,
    "time_elapsed": times
})
df.to_csv("times.csv", index=False)