import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("times.csv")
file = "Thread_Metrics"

#Threads vs Speedup Plot
plt.figure(figsize=(10,6))
for a in sorted(df['N'].unique()):
    x = df[df['N'] == a]['threads']
    y = df[df['N'] == a]['speedup']
    plt.plot(x, y, marker='o', label=f"N = {a}")

plt.xticks([1, 2, 4, 8, 16, 32])
plt.xlabel("Threads")
plt.ylabel("Speedup")
plt.title("Threads vs Speedup")
plt.grid(True)
plt.legend()
plt.savefig(f"{file}/Threads_vs_Speedup_Plot.png")

#Threads vs Efficiency
plt.figure(figsize=(10,6))
for a in sorted(df['N'].unique()):
    x = df[df['N'] == a]['threads']
    y = df[df['N'] == a]['efficiency']
    plt.plot(x, y, marker='o', label=f"N = {a}")

plt.xticks([1, 2, 4, 8, 16, 32])
plt.xlabel("Threads")
plt.ylabel("Efficiency")
plt.title("Threads vs Efficiency")
plt.grid(True)
plt.legend()
plt.savefig(f"{file}/Threads_vs_Efficiency_Plot.png")

#Threads vs Time
plt.figure(figsize=(10,6))
for a in sorted(df['N'].unique()):
    x = df[df['N'] == a]['threads']
    y = df[df['N'] == a]['time_elapsed']
    plt.plot(x, y, marker='o', label=f"N = {a}")

plt.xticks([1, 2, 4, 8, 16, 32])
plt.xlabel("Threads")
plt.ylabel("Time")
plt.title("Threads vs Time")
plt.grid(True)
plt.legend()
plt.savefig(f"{file}/Threads_vs_Time_Plot.png")

#Computational Cost
plt.figure(figsize=(10,6))
for a in sorted(df['N'].unique()):
    x = df[df['N'] == a]['threads']
    y = df[df['N'] == a]['computational_cost']
    plt.plot(x, y, marker='o', label=f"N = {a}")

plt.xticks([1, 2, 4, 8, 16, 32])
plt.xlabel("Threads")
plt.ylabel("Computational Cost")
plt.title("Computational Cost by N")
plt.grid(True)
plt.legend()
plt.savefig(f"{file}/Computational_Cost.png")