import matplotlib.pyplot as plt
with open("times.txt", "r") as file:
    # Read each line, convert to int (or float), and double it
    numbers = [float(line.strip()) * 2 for line in file]

plt.figure(figsize=(10,6))

plt.hist(numbers, bins = 20, edgecolor='black')
plt.title("N = 1000, Threads = 32")
plt.xlabel("Seconds")

plt.show()