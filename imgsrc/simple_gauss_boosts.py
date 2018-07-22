import plotfonts
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def compute_times_speeds(times):
    dt = times[1] - times[0]
    new_times = np.array([0])
    speeds = np.array([0])
    for time in times[1:]:
        new_times = np.append(new_times, time)
        new_times = np.append(new_times, time)
        speeds = np.append(speeds, speeds[-1])
        speeds = np.append(speeds, speeds[-1] + dt * 250)
    return new_times[:-1], speeds[:-1]

def init():
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 2000)
    return ln, guideline

def update(frame):
    xdata, ydata = compute_times_speeds(np.linspace(0, TIME_MAX, frame))
    ln.set_data(xdata, ydata)
    return ln, guideline

TIME_MAX = 8

fig, ax = plt.subplots()
fig.set_figwidth(6)
fig.set_figheight(4)
xdata, ydata = [], []
ln, = plt.plot([], [], animated=True, label='Discrete boosting')
guideline, = ax.plot([0, 8], [0, 2000], 'gray', animated=True, label='Continuous boosting')

ax.grid(True)
init()

plt.xlabel('Time (s)')
plt.ylabel('Horizontal speed (ups)')
plt.tight_layout()
plt.legend(loc=0)

ani = FuncAnimation(fig, update, frames=np.arange(3, 18),
                    init_func=init, blit=True)
ani.save('simple_gauss_boosts.gif', dpi=110, writer='imagemagick')
plt.show()
