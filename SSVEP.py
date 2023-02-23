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

#ADC Params
ACQTIME = 5
SPS = 860 #samples per second
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

#ADC Setup
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
adc = ADS.ADS1115(i2c)
adc.mode = ADS.Mode.CONTINUOUS
adc.gain = 1
adc.data_rate = SPS
raw_signal = np.zeros(nsamples)
chan = AnalogIn(adc, ADS.P2, ADS.P3)

fr1, fr2, fr3, fr4 = 8, 10, 12, 14 

while True:
	blinking_circles("a","b","c","d",fr1,fr2,fr3,fr4)
	for i in range(nsamples): #Collects data every interval
		st = time.perf_counter()
		raw_signal[i] = chan.value*(4.096/32767)
		raw_signal[i] -= 3.3 #ADC ground is 3.3 volts above circuit ground
		while (time.perf_counter() - st) <= sinterval:
			pass

	t = time.perf_counter() - t0

	ps1, rms1 = rms_voltage_power_spectrum(raw_signal, fr1, fr1, SPS, nsamples)
	ps2, rms2 = rms_voltage_power_spectrum(raw_signal, fr2, fr2, SPS, nsamples)
	ps3, rms3 = rms_voltage_power_spectrum(raw_signal, fr3, fr3, SPS, nsamples)
	ps4, rms4 = rms_voltage_power_spectrum(raw_signal, fr4, fr4, SPS, nsamples)

	largest = max(rms1,rms2,rms3,rms4)

	print("rms 1: ", rms1)
	print("rms 2: ", rms2)
	print("rms 3: ", rms3)
	print("rms 4: ", rms4)

	if (largest == rms1):
		print("You're looking at: ", fr1, "Hz")
	elif (largest == rms2):
		print("You're looking at: ", fr2, "Hz")
	elif (largest == rms3):
		print("You're looking at: ", fr3, "Hz")
	elif (largest == rms4):
		print("You're looking at: ", fr4, "Hz")


