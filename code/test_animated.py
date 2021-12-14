import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


fig, ax = plt.subplots()
xdata, ydata0, ydata1 = [], [], []
ln0, = plt.plot([], [], 'r', animated=True)
ln1, = plt.plot([], [], 'b', animated=True)
f = np.linspace(-3, 3, 200)


def init():
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.25, 10)
    ln0.set_data(xdata,ydata0)
    ln1.set_data(xdata,ydata1)
    return ln0, ln1


def update(frame):
    xdata.append(frame)
    ydata0.append(np.exp(-frame**2))
    ydata1.append(np.exp(frame**2))
    ln0.set_data(xdata, ydata0)
    ln1.set_data(xdata, ydata1)
    return ln0, ln1,


ani = FuncAnimation(fig, update, frames=f,
                    init_func=init, blit=True, interval=2.5, repeat=False)
plt.show()