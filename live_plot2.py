import matplotlib.pyplot as plt
from drawnow import drawnow
import numpy as np

def make_fig():
    plt.scatter(x, y)  # I think you meant this

plt.ion()  # enable interactivity
fig = plt.figure()  # make a figure

x = list()
y = list()

for i in range(1000):
    temp_y = np.random.random()
    x.append(i)
    y.append(temp_y)  # or any arbitrary update to your figure's data
    i += 1
    drawnow(make_fig)
