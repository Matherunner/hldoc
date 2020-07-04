import plotfonts
import numpy as np
import matplotlib.pyplot as plt

frate = np.linspace(1, 1000, 100000)
ratio = 1000 / np.floor(1000 / frate) / frate

plt.figure(figsize=(6, 3))
plt.plot(frate, ratio, 'k', lw=0.7)
plt.xlim((0, 1000))
plt.ylim((1, 2))
plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
plt.yticks([1, 1.5, 2])
# plt.xscale('log')
plt.xlabel('frame rate')
plt.ylabel('slow-down factor')
plt.grid(True)
plt.tight_layout()
plt.savefig('frame_rate_unsync.png', dpi=220, transparent=True)
plt.show()
