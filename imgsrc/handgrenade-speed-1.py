import plotfonts
import numpy as np
import matplotlib.pyplot as plt

def gpitch(pitch):
    if pitch < 0:
        return -10 + 8 / 9 * pitch
    return -10 + 10 / 9 * pitch

# pitch is in degrees
def gvel(pitch):
    gp = gpitch(pitch)
    scale = min(500, 360 - 4 * gp)
    return scale

pitch = np.linspace(-180, 180, 10000)
gspeeds = []
for p in pitch:
    gspeeds.append(gvel(p))
gspeeds = np.array(gspeeds)

plt.plot(pitch, gspeeds)
plt.grid()
plt.show()
