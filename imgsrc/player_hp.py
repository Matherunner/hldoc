import plotfonts
import numpy as np
import matplotlib.pyplot as plt

H = 100.
A = 40.

dmg = np.linspace(0, 200, 4000)
armour = np.array([max(0, A - 2 * d / 5) for d in dmg])
health = H - np.array([int(d / 5) if a != 0 else int(d - 2 * A) for a, d in zip(armour, dmg)])

plt.figure(figsize=(5, 4))
plt.plot(dmg, health, 'r', label='Health')
plt.plot(dmg, armour, 'b', label='Armour')
plt.xlim((0, dmg[-1]))
plt.xlabel('Damage')
plt.grid(True)
plt.legend(loc=0)
plt.tight_layout()
plt.savefig('player_hp.png', dpi=200, transparent=True)
plt.show()
