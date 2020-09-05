import matplotlib.pyplot as plt
import plotfonts
import numpy as np

data = np.genfromtxt('agstplot.txt', delimiter=',')

plt.figure(figsize=(8, 5))
plt.plot(data[:, 0], data[:, 1], label='Air')
plt.plot(data[:, 0], data[:, 2], label='Ground')
plt.grid()
plt.legend(loc=0)
plt.ylabel('Acceleration')
plt.xlabel('Speed')
plt.tight_layout()
plt.savefig('agstplot.pdf', transparent=True)
