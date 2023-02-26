
import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd())) #Allows importing files from parent folder
import time
import pickle
import threading
import multiprocessing
import numpy as np
import scipy as sp
from scipy import signal
from scipy.signal import butter, sosfilt
import matplotlib.pyplot as plt

from openai_application import get_prompts
import openai
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import pyttsx3
import speech_recognition as sr
from gui import blinking_circles
from signal_tools import rms_voltage_power_spectrum, brain_signal_extraction
from speech_tools import speech_to_text, text_to_speech
from openai_application import get_prompts

openai.api_key = "INSERT API KEY HERE"

#ADC Params
ACQTIME = 8
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

FR1, FR2, FR3, FR4 = 8, 10, 12, 14 

def data(prompt_1, prompt_2, prompt_3, prompt_4):
	t0 = time.perf_counter()
	for i in range(nsamples): #Collects data every interval
		st = time.perf_counter()
		raw_signal[i] = chan.value*(4.096/32767)
		raw_signal[i] -= 3.3 #ADC ground is 3.3 volts above circuit ground
		while (time.perf_counter() - st) <= sinterval:
			pass
	t = time.perf_counter() - t0

	ps1, rms1 = rms_voltage_power_spectrum(raw_signal, FR1, FR1, SPS, nsamples)
	ps2, rms2 = rms_voltage_power_spectrum(raw_signal, FR2, FR2, SPS, nsamples)
	ps3, rms3 = rms_voltage_power_spectrum(raw_signal, FR3, FR3, SPS, nsamples)
	ps4, rms4 = rms_voltage_power_spectrum(raw_signal, FR4, FR4, SPS, nsamples)
	
	print("rms 1: ", rms1)
	print("rms 2: ", rms2)
	print("rms 3: ", rms3)
	print("rms 4: ", rms4)
	
	largest = max(rms1,rms2,rms3,rms4)
	
	if (largest == rms1):
		return prompt_1
	elif (largest == rms2):
		return prompt_2
	elif (largest == rms3):
		return prompt_3
	elif (largest == rms4):
		return prompt_4
	else:
		return "what"


if __name__ == "__main__":
	engine = pyttsx3.init()
	engine.setProperty('rate', 150)
	engine.setProperty('volume', 0.7)
	recognizer = sr.Recognizer()
		

	# Step 1 - Prompt User to Initiate Conversation
	text_to_speech(engine, "Hello, fancy a conversation?")
	
	while True:
		
		speech = speech_to_text(recognizer)
		print(speech)
		choice = "More Options"
		
		while choice == "More Options":
			prompt_1, prompt_2, prompt_3, prompt_4 = get_prompts(speech)
			print(prompt_1)
			print(prompt_2)
			print(prompt_3)
			print(prompt_4)
			
			process1 = multiprocessing.Process(
					target=blinking_circles, 
					args=(
						prompt_1, prompt_2, prompt_3, prompt_4, FR1, FR2, FR3, FR4
					)
				)
			
			process1.start() # GUI Appears on screen with prompts
			
			choice = data(prompt_1, prompt_2, prompt_3, prompt_4) # SSVEP data collection to get response

		text_to_speech(engine, choice)



	


	





