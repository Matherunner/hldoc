import math
import numpy as np
import matplotlib.pyplot as plt

def strafe_maxaccel(speed, L, tau, M, A):
    tauMA = tau * M * A
    LtauMA = L - tauMA
    if LtauMA <= 0:
        return math.sqrt(speed * speed + L * L)
    elif LtauMA <= speed:
        return math.sqrt(speed * speed + tauMA * (L + LtauMA))
    else:
        return speed + tauMA

speed = 3000
framerates = np.linspace(1, 1000, 1000)
newspeeds = []
for fr in framerates:
    newspeeds.append(strafe_maxaccel(speed, 30, 1 / fr, 320, 10))
newspeeds = np.array(newspeeds)
accels = (newspeeds - speed) * framerates

plt.plot(framerates, accels)
plt.grid()
plt.show()
