time = [31.314, 34.248, 29.348, 25.453, 26.566, 25.480, 26.121, 23.838]

from matplotlib import pyplot as plt

plt.plot(range(1, 9), time)
plt.title("Comparison of Time taken with increasing number of processors")
plt.ylabel("Time Taken")
plt.xlabel("Number of Processors being used")
plt.show()
