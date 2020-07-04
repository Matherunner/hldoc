import plotfonts
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def strafe_speed(v, L, tauMA, theta):
    gamma1 = tauMA
    gamma2 = L - v * np.cos(theta)
    if gamma2 < 0:
        return v
    mu = min(gamma1, gamma2)
    return np.sqrt(v * v + mu * mu + 2 * v * mu * np.cos(theta))

def opt_theta(v, L, tauMA):
    tmp = L - tauMA
    if tmp < 0:
        return np.pi
    if tmp < v:
        return np.arccos(tmp / v)
    return 0

def genpoints(v, L, tau, MA):
    tauMA = tau * MA
    thetas = np.linspace(0, 2 * np.pi, 4000)
    speeds = np.array([strafe_speed(v, L, tauMA, theta) for theta in thetas])
    accels = (speeds - v) / tau
    return thetas, accels

def update_line(frame, line, optline1, optline2, dots, text):
    L = 30
    tau = 0.001
    MA = 320 * 10
    
    v = frame
    thetas, accels = genpoints(v, L, tau, MA)
    line.set_data(thetas, accels)
    optang = opt_theta(v, L, tau * MA)
    optline1.set_data([optang] * 2, [0, 4000])
    optline2.set_data([-optang] * 2, [0, 4000])
    dots.set_data([optang, -optang], [4000] * 2)
    text.set_text(f'{int(v)} ups')
    return line, optline1, optline2, dots, text

# thetas, accels = genpoints(200, 30, 0.01, 320 * 10)
# plt.polar(thetas, accels)

fig = plt.figure(figsize=(3.5, 3.5))

line, = plt.polar([], [], color='darkblue', label='Acceleration')
optline1, = plt.polar([], [], color='gray', dashes=[5, 3], lw=1)
optline2, = plt.polar([], [], color='gray', dashes=[5, 3], lw=1)
dots, = plt.polar([], [], 'o', color='darkred')
text = plt.text(np.deg2rad(70), 4500, '', color='darkblue')

plt.ylim((-4000, 4000))
# plt.yticks([-4000, -2000, 0, 2000, 4000])
plt.yticks([0, 4000, -4000])
    
line_ani = FuncAnimation(
    fig, update_line, 80,
    fargs=(line, optline1, optline2, dots, text),
    interval=200, blit=False)
line_ani.save('strafe-plots.gif', dpi=110, writer='imagemagick')

plt.tight_layout()
plt.show()
