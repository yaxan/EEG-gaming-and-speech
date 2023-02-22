import os
import sys
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt 
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import scipy as sp
from scipy import signal
from analysis_data import rms_voltage_power_spectrum, brain_signal_extraction

ACQTIME = 5
SPS = 860 #samples per second
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
adc = ADS.ADS1115(i2c)
adc.mode = ADS.Mode.CONTINUOUS
adc.gain = 1
adc.data_rate = SPS



raw_signal = np.zeros(nsamples)
t0 = time.perf_counter()
chan = AnalogIn(adc, ADS.P2, ADS.P3)

for i in range(nsamples): #Collects data every interval
	st = time.perf_counter()
	raw_signal[i] = chan.value*(4.096/32767)
	raw_signal[i] -= 3.3 #ADC ground is 3.3 volts above circuit ground
	while (time.perf_counter() - st) <= sinterval:
		pass
		
fr1, fr2, fr3 = 10, 15, 20, 

t = time.perf_counter() - t0
ps, rms = rms_voltage_power_spectrum(raw_signal, fr1, fr1, SPS, nsamples)
ps2, rms2 = rms_voltage_power_spectrum(raw_signal, fr2, fr2, SPS, nsamples)
ps3, rms3 = rms_voltage_power_spectrum(raw_signal, fr3, fr3, SPS, nsamples)
#ps4, rms4 = rms_voltage_power_spectrum(raw_signal, fr4, fr4, SPS, nsamples)

ps, rmsh = rms_voltage_power_spectrum(raw_signal, (fr1)-0.5, (fr1)+0.5, SPS, nsamples)
ps2, rms2h = rms_voltage_power_spectrum(raw_signal, (fr2)-0.5, (fr2)+0.5, SPS, nsamples)
ps3, rms3h = rms_voltage_power_spectrum(raw_signal, (fr3)-0.5, (fr3)+0.5, SPS, nsamples)

rms1Total = rms
rms2Total = rms2
rms3Total = rms3


largest = max(rms1Total,rms2Total,rms3Total)

print("rms 1: ", rms1Total)
print("rms 2: ", rms2Total)
print("rms 3: ", rms3Total)
#print("rms 3: ", rms4)

if (largest == rms1Total):
	print("You're looking at: ", fr1, "Hz")
elif (largest == rms2Total):
	print("You're looking at: ", fr2, "Hz")
elif (largest == rms3Total):
	print("You're looking at: ", fr3, "Hz")

