"""
Live plotting
"""

import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import time
import numpy as np
import matplotlib.pyplot as plt
from adafruit_ads1x15.ads1x15 import ADS1x15
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio
import scipy as sp
import keyboard

SPS = 860 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
sinterval = 1.0/SPS
freq_min = 8 #min freq of alpha waves
freq_max = 12 #max freq of alpha waves

plt.ion() ## Note this correction
fig=plt.figure()
plt.axis([0,10,-1,1])

i = 0
t=list()
y=list()


i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

print()
print('Initializing ADC...')
print()

adc = ADS.ADS1115(i2c)
adc.mode = Mode.CONTINUOUS
adc.gain = 1
adc.data_rate = SPS

print("press q to exit program")

while True: #Loops every time user records data

    st = time.perf_counter()

    chan = AnalogIn(adc, ADS.P2, ADS.P3)
    y.append(chan.value*(4.096/32767) - 3.3) #ADC ground is 3.3 volts above circuit ground
    t.append(time.perf_counter())

    plt.plot(t, y, c = 'b')
    plt.show()
    plt.pause(0.1)

    while (time.perf_counter() - st) <= sinterval:
        pass

    if keyboard.is_pressed('q'):
        break