import plotfonts
import numpy as np
import matplotlib.pyplot as plt

def ladder_yaw(alpha, S, F, vz):
    nx = np.cos(alpha)
    nz = np.sin(alpha)
    return np.arctan2(-np.copysign(1, S * vz), -np.copysign(1, F * vz) * np.sqrt(2 * nz * nx))

def ladder_pitch(alpha, S, F, vz):
    nx = np.cos(alpha)
    nz = np.sin(alpha)
    return -np.copysign(1, F * vz * (1 / np.sqrt(2) - nz)) * np.arccos(np.sqrt(2 * nz * nx))

alphas = np.linspace(0, np.pi / 2, 100000)
yaws = ladder_yaw(alphas, 200, 200, 1)
pitches = ladder_pitch(alphas, 200, 200, 1)

yaws = np.rad2deg(yaws)
pitches = np.rad2deg(pitches)
zipped = np.stack((yaws, pitches))

#plt.figure(figsize=(6, 3))
plt.figure(figsize=(2.5, 5))
plt.axes().set_aspect('equal')
plt.plot(zipped[0], zipped[1], 'k')

for a in [5, 15, 30, 45, 60, 75, 85]:
    alpha = np.deg2rad(a)
    yaw = np.rad2deg(ladder_yaw(alpha, 200, 200, 1))
    pitch = np.rad2deg(ladder_pitch(alpha, 200, 200, 1))
    plt.plot(yaw, pitch, 'ok')
    plt.text(yaw + 5, pitch, rf'α = {a}', verticalalignment='center')

plt.xlim((-150, -90))
plt.ylim((-90, 90))
plt.xticks([-150, -130, -110, -90])
plt.yticks(np.arange(-90, 91, 30))
plt.xlabel('yaw')
plt.ylabel('pitch')
plt.grid()
plt.tight_layout()
plt.savefig('ladder-angles-1.png', dpi=200, transparent=True)
plt.show()
