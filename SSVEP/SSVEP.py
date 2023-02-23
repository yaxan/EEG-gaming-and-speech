import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #Allows importing files from parent folder
import time
import pickle
import threading
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import scipy as sp
from scipy import signal
from scipy.signal import butter, sosfilt
from adafruit_ads1x15.analog_in import AnalogIn
from gui import blinking_circles
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

def data():
	t0 = time.perf_counter()
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
	
	print("rms 1: ", rms1)
	print("rms 2: ", rms2)
	print("rms 3: ", rms3)
	print("rms 4: ", rms4)
	
	rms1, rms2, rms3, rms4;
	
	largest = max(rms1,rms2,rms3,rms4)

	if (largest == rms1):
		print("You're looking at: ", fr1, "Hz")
	elif (largest == rms2):
		print("You're looking at: ", fr2, "Hz")
	elif (largest == rms3):
		print("You're looking at: ", fr3, "Hz")
	elif (largest == rms4):
		print("You're looking at: ", fr4, "Hz")
		
def gui():
	blinking_circles("a", "b", "c", "d", fr1, fr2, fr3, fr4)
	
	
if __name__ == "__main__":
	
	process1 = multiprocessing.Process(target=gui)
	
	process1.start()
	
	data()

	process1.terminate()


	





