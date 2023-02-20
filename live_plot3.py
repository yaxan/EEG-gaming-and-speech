import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Set up the figure and subplot
fig, ax = plt.subplots()

# Initialize the line that will be plotted
line, = ax.plot([], [], lw=2)

# Set the x-axis limits
ax.set_xlim(0, 4*np.pi)

# Set the y-axis limits
ax.set_ylim(-1, 1)

# Define the function that will be called to update the plot
def update(frame):
    # Generate some data
    x = np.linspace(0, 4*np.pi, 1000)
    y = np.sin(x - frame/10.0)

    # Update the line data
    line.set_data(x, y)

    # Return the line object
    return line,

# Create an animation object
anim = FuncAnimation(fig, update, frames=200, interval=50)

# Show the plot
plt.show()
