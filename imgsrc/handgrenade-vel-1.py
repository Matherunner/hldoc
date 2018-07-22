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
    gp = np.deg2rad(gp)
    return [scale * np.cos(gp), -scale * np.sin(gp)]

pitch = np.linspace(-180, 180, 10000)
gvels = []
for p in pitch:
    gvels.append(gvel(p))
gvels = np.array(gvels)

plt.figure(figsize=(6, 4))
plt.axes().set_aspect('equal')
plt.plot(gvels[:, 0], gvels[:, 1], 'k')

for pitch, offs in [[-180, (10, 5)], [-135, (10, -10)], [-90, (0, -30)],
                    [-60, (10, 10)], [-28.125, (-150, -10)], [0, (15, 0)],
                    [30, (15, -20)], [60, (-70, -15)], [90, (-70, 0)],
                    [120, (-70, 20)], [150, (15, 15)], [180, (15, 0)]]:
    vel = gvel(pitch)
    plt.plot(vel[0], vel[1], 'ok')
    paren = '' if pitch != -180 else ' (player pitch)'
    plt.text(vel[0] + offs[0], vel[1] + offs[1], fr'{pitch}°{paren}'.replace('-', '−'), verticalalignment='center')

plt.xlim((-550, 500))
plt.xticks(np.arange(-500, 501, 100))
plt.xlabel('relative horizontal velocity')
plt.ylabel('relative vertical velocity')
plt.grid()
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig('handgrenade-vel-1.png', dpi=200, transparent=True)
plt.show()
