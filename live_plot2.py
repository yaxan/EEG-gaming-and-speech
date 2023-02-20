"""
Live plotting
"""

import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import time
from random import random

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

SPS = 860 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
sinterval = 1.0/SPS

t=list()
y=list()
z=list()

fig, axs =plt.subplots(1, 2)
axs[0].set(ylim=(-1, 1))
axs[1].set(ylim=(-1, 1))


print("press q to exit program")

while True: #Loops every time user records data

    st = time.perf_counter()

    chan = random() - 0.5

    y.append(chan)
    #print(chan)
    t.append(time.perf_counter())

    if time.perf_counter() > 10 and len(t) > 20:
        t.pop(0)
        y.pop(0)
        axs[0].set_xlim(t[-1]-10, t[-1])
        axs[1].set_xlim(t[-1]-10, t[-1])

    z = [x + 0.2 for x in y]

    axs[0].plot(t, y, c = 'b')  
    axs[1].plot(t, z, c = 'r')
    
    # Render the plot to an RGBA buffer
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()

    # Convert the buffer to a NumPy array
    w, h = canvas.get_width_height()
    arr = np.frombuffer(buf, dtype=np.uint8).reshape((h, w, 4))

    # Convert the RGBA image to an RGB image
    img = cv2.cvtColor(arr, cv2.COLOR_RGBA2RGB)

    # Display the image using OpenCV
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    while (time.perf_counter() - st) <= sinterval:
        pass

    del buf
    del arr

    if key == ord('q'):
        break

cv2.destroyAllWindows()
