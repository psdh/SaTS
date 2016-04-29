cpu = [112, 171, 208, 252, 269, 275, 300, 338]

from matplotlib import pyplot as plt

plt.plot(range(1, 9), cpu)
plt.plot(range(1, 9), range(100, 900, 100))
plt.title("Comparison of y=x and CPU usage as number of processors are increased")
plt.xlabel("Number of Processors being used")
plt.ylabel("Percentage of CPU use")
plt.show()
