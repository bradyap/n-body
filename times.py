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
    print(f'\r|{bar}| {percent*100:.01f}% Completed  N = {N}', end='', flush=True)

G = 0.001
DT = 0.001
N_list = [500, 1000, 2000, 4000, 5000]
threads_list = [1,2,4,8,16,32]

pos_min, pos_max = -50, 50
vel_min, vel_max = -1, 1
mass_min, mass_max = 0.1, 10

times_N = []
times_thread = []
times = []
speedup = []
efficiency = []
computational_cost = []

count = 0
for N in N_list:
    bodies = nbody.BodiesContainer(N)

    pos = np.random.uniform(pos_min, pos_max, (N, 3))
    vel = np.random.uniform(vel_min, vel_max, (N, 3))
    mass = np.random.uniform(mass_min, mass_max, N)

    #bodies.set_all(pos[:,0], pos[:,1], pos[:,2], vel[:,0], vel[:,1], vel[:,2], mass)

    for threads in threads_list:
        bodies.set_all(pos[:,0], pos[:,1], pos[:,2], vel[:,0], vel[:,1], vel[:,2], mass)

        duration = nbody.benchmark_threaded(bodies, DT, G, threads, 100)
        count += 1

        percentage_bar(count, int(len(N_list)*len(threads_list)), N)

        times_N.append(N)
        times_thread.append(threads)
        times.append(duration)

print("")
true_time = {}
for i in range(len(times_N)):
    N_val = times_N[i]
    threads_val = times_thread[i]
    times_val = times[i]

    if threads_val == 1:
        true_time[N_val] = times_val
        speedup.append(1)
        efficiency.append(1)
    else:
        speedup.append(true_time[N_val]/times_val)
        efficiency.append((true_time[N_val]/times_val)/threads_val)

    computational_cost.append(times_val/(N_val**2))

df = pd.DataFrame({
    "N": times_N,
    "threads": times_thread,
    "time_elapsed": times,
    "speedup": speedup,
    "efficiency": efficiency,
    "computational_cost":computational_cost
})
df.to_csv("times.csv", index=False)