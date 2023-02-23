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
import csv
import pandas as pd

#import files from parent folder
sys.path.insert(1, os.path.dirname(os.getcwd())) 

ACQTIME = 5
SPS = 860 #samples per second
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS
min_freq = 8 #min freq of alpha waves
max_freq = 8 #max freq of alpha waves

#create ADC Object
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
adc = ADS.ADS1115(i2c)
adc.mode = ADS.Mode.CONTINUOUS
adc.gain = 1
adc.data_rate = SPS
        
folder = input('Please input folder:')
path = os.path.join(folder)
if not os.path.isdir(path): 
    try:
        os.mkdir(path)
        print("Folder Created")
    except OSError:
        print("Failed to create folder: %s" % path)
else:
    print("Successfully connected to folder: %s" % path)
    
while True:
    data = input('Please type 8 10 12 or 14')
    if data in ['8','10','12', '14']:
        break   
    else:
        print('Please type 8 10 12 or 14')                   
if data == '8':
    file_path = os.path.join(path,'8Hz.csv')
elif data == '10':
    file_path = os.path.join(path,'10Hz.csv')
elif data == '12':
    file_path = os.path.join(path,'12Hz.csv')
elif data == '14':
    file_path = os.path.join(path,'14Hz.csv')

stopper = 'n'
while stopper != 'y': #Loops every time user records data

    input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
    print()
    #adc.read(2, True)
    time_series = np.zeros(nsamples, 'float')
    sos = butter(10, 60, 'lowpass', fs=860, output='sos')
    
    t0 = time.perf_counter()
    for i in range(nsamples): #Collects data every sinterval
        startime = time.perf_counter()
        chan = AnalogIn(adc, ADS.P2, ADS.P3)
        time_series[i] = chan.value*(4.096/32767)
        time_series[i] -= 3.3 #ADC ground is 3.3 volts above circuit ground
        while (time.perf_counter() - startime) <= sinterval:
            pass
    filtered = sp.signal.sosfilt(sos,time_series)
    t = time.perf_counter() - t0    
    print('Time elapsed: %.9f s.' % t)

    freq = np.fft.fftfreq(nsamples, d=1.0/SPS)
    ps, rms = rms_voltage_power_spectrum(filtered, min_freq, max_freq, SPS, nsamples)
    print('RMS of Alpha Wave Voltage: ', rms)
    
    fig, ax = plt.subplots(ncols=3, nrows=1, figsize=[25,10])
    times = np.arange(0, ACQTIME, sinterval)
    
    ax[0].plot(times, filtered)
    ax[0].set(xlabel='Time (s)', ylabel='Voltage', title='Raw Signal of Brain Waves') 
       
    ax[1].set_xlim((0,200))
    ax[1].set(xlabel='Frequency (Hz)', ylabel='Power', title='Power Spectrum')  
    ax[1].plot(freq, ps)
    
    brain_wave = brain_signal_extraction(filtered, min_freq, max_freq, freq)  
    ax[2].plot(times, brain_wave)
    ax[2].set(xlabel='Time (s)', ylabel='Voltage', title='Brain Alpha Wave')    
    fig.show()
    
    while True:
        save_data = input('Save this last run? (y/n)')
        if save_data == 'y':
            #append to exisiting
            if os.path.exists(file_path): 
                with open(file_path, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(time_series)

                    df = pd.read_csv(file_path, header=None)
                    print(df.count()[0])
            #create a new file
            else: 
                with open(file_path, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(time_series)
            break            
        elif save_data == 'n':
            break
        else:
            print('Please type (y/n)')
    plt.close('all')
    while True:
        stopper = input('Press a button to end the process')
        if stopper:
            break
        else:
            print('Press a button to end the process')
    print('\n')
