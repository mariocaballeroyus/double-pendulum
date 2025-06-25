import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .datareader import DataReader

def animate_pendulum(datareader: DataReader, show=True):
    """
    Animates the double pendulum with marker sizes proportional to mass.
    Masses and interval are read from the data object's parameters attribute.
    """
    # Get masses and interval from data.parameters (default if missing)
    params = datareader.parameters
    mass1 = params["mass1"] if "mass1" in params else 1.0
    mass2 = params["mass2"] if "mass2" in params else 1.0
    interval = params["time:step"] * 1e-3 if "time:step" in params else 10

    # Read positions from the datareader
    pos = datareader[["x1", "y1", "x2", "y2"]]

    # Animation setup
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    margin = 0.2
    x_min = np.min(pos[:, [0, 2]]) - margin
    x_max = np.max(pos[:, [0, 2]]) + margin
    y_min = np.min(pos[:, [1, 3]]) - margin
    y_max = np.max(pos[:, [1, 3]]) + margin
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([])
    ax.set_yticks([])

    # Scale marker sizes proportional to mass
    base_size = 20
    ms1 = base_size
    ms2 = base_size * (mass2 / mass1) if mass1 != 0 else base_size

    # Prepare the line and markers
    line, = ax.plot([], [], '-', lw=2, color='k')
    m1_dot = ax.plot([], [], 'o', color='b', markersize=ms1)[0]
    m2_dot = ax.plot([], [], 'o', color='g', markersize=ms2)[0]
    trace, = ax.plot([], [], 'r-', lw=1, alpha=0.5)

    #  Update function for the trace
    def update(i):
        x = [0, pos[i, 0], pos[i, 2]]
        y = [0, pos[i, 1], pos[i, 3]]
        line.set_data(x, y)
        m1_dot.set_data([x[1]], [y[1]])
        m2_dot.set_data([x[2]], [y[2]])
        trace.set_data(pos[:i+1, 2], pos[:i+1, 3])
        return line, m1_dot, m2_dot, trace

    # Create the animation
    animation = FuncAnimation(fig, update, frames=len(pos), interval=interval, blit=True)

    if show:
        plt.show()

    return animation