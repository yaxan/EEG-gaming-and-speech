"""
Live plotting
"""

import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import time
import matplotlib.pyplot as plt

plt.ion() ## Note this correction
fig=plt.figure()
plt.axis([0,10,-1,1])

SPS = 860 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
sinterval = 1.0/SPS

i = 0
t=list()
y=list()


print("press q to exit program")

while True: #Loops every time user records data

    st = time.perf_counter()

    chan = 0.45
    y.append(chan)
    t.append(time.perf_counter())

    plt.plot(t, y, c = 'b')
    plt.show()
    plt.pause(0.1)

    while (time.perf_counter() - st) <= sinterval:
        pass