import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("times.csv")

print(df)

plt.figure(figsize=(10,6))

plt.plot(df['N'], df['time_elapsed'], marker='o')
plt.xticks(df['N'])

plt.grid(True)
plt.title("Times for N")
plt.xlabel("N")
plt.ylabel("Time")
plt.savefig("Serial_Metrics/Serial_Times.png")
