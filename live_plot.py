"""
Live plotting
"""

import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from adafruit_ads1x15.ads1x15 import ADS1x15
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio
import itertools

SPS = 860 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
sinterval = 1.0/SPS
freq_min = 8 #min freq of alpha waves
freq_max = 12 #max freq of alpha waves


i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

print()
print('Initializing ADC...')
print()

adc = ADS.ADS1115(i2c)
adc.mode = Mode.CONTINUOUS
adc.gain = 1
adc.data_rate = SPS

print("press q to exit program")

fig, ax = plt.subplots(1, 1)
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

t = list()
y = list()

ot = time.perf_counter()

def update(frame):
    st = time.perf_counter()
    
    ot = st if len(t) == 0 else None     
    
    chan = AnalogIn(adc, ADS.P2, ADS.P3)
    t.append(st-ot)
    y.append(chan.value*(4.096/32767) - 3.3) #ADC ground is 3.3 volts above circuit ground

    if t[-1] > 10:
        t.pop(0)
        y.pop(0)
        
    print(st)

    line.set_data(t, y)

    return line,

anim = FuncAnimation(fig, update, frames=itertools.count(), interval=sinterval*1e3)
plt.show()
