
import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import numpy as np
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt
import pickle
from analysis_data import rms_voltage_power_spectrum, brain_signal_extraction

#These values should match saved data being loaded
ACQTIME = 5
SPS = 860 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
nsamples = ACQTIME*SPS
sinterval = 1.0/SPS
freq_min = 8
freq_max = 12 
freq = np.fft.fftfreq(nsamples, d=1.0/SPS)
times = np.arange(0, ACQTIME, sinterval)

while True:        
    save_folder = input('Please input folder name to load:')
    save_path = os.path.join(save_folder)
    if os.path.isdir(save_path): #Check if already a directory
        break
    else:
        print("Please enter an existing folder name")

#Load File
relaxed_file = os.path.join(save_path,'relaxed.pickle')
concentrated_file = os.path.join(save_path,'concentrated.pickle')

file1 = open(relaxed_file, 'rb')
relaxed_data = pickle.load(file1) 
file1.close()
relaxed_data = np.array(relaxed_data) 
file2 = open(concentrated_file, 'rb')
concentrated_data = pickle.load(file2)
file2.close()
concentrated_data = np.array(concentrated_data)

frequencies = fftfreq(nsamples, d=1.0/SPS)
#gather voltage rms values to plot 
relaxed_rms = np.zeros(relaxed_data.size)
concentrated_rms = np.zeros(concentrated_data.size)
for i, time_series in enumerate(relaxed_data):
    ps, rms = rms_voltage_power_spectrum(time_series, freq_min, freq_max, SPS, nsamples)
    relaxed_rms[i] = rms
    if i == 0: ps1 = ps #store the first power spectrum values to plot 
for i, time_series in enumerate(concentrated_data):
    ps, rms = rms_voltage_power_spectrum(time_series, freq_min, freq_max, SPS, nsamples)
    concentrated_rms[i] = rms
    if i == 0: ps2 = ps

relaxed = relaxed_data[0]
brain_relaxed = brain_signal_extraction(relaxed, 8, 12, frequencies)
concentrated = concentrated_data[0]
brain_concentrated = brain_signal_extraction(concentrated, 8, 12, frequencies)

#Plot Raw Data
fig, ax = plt.subplots(ncols=2, nrows=1, figsize=[10,5])
ax[0].plot(times, relaxed)
ax[0].set(xlabel='Time (s)', ylabel='Voltage (V)', title='Relaxed State')
ax[1].plot(times, concentrated, color='red')
ax[1].set(xlabel='Time (s)', ylabel='Voltage (V)', title='Concentrated State')

#Plot Power Spectrum
ps_relaxed = ps1
ps_concentrated = ps2
fig2, ax2 = plt.subplots(ncols=2, nrows=1, figsize=[10,5])
ax2[0].plot(frequencies[0:250], ps_relaxed[0:250])
ax2[0].set(xlabel='Frequency (Hz)', ylabel='Power', title='R.S. Power Spectrum')
ax2[1].plot(frequencies[0:250], ps_concentrated[0:250], color='red')
ax2[1].set(xlabel='Frequency (Hz)', ylabel='Power', title='C.S. Power Spectrum')

#Plot Pure Brain Wave
fig3, ax3 = plt.subplots(ncols=2, nrows=1, figsize=[10,5])
ax3[0].plot(times, brain_relaxed)
ax3[0].set(xlabel='Time (s)', ylabel='Voltage (V)', title='R.S. Brain Wave')
ax3[1].plot(times, brain_concentrated, color='red')
ax3[1].set(xlabel='Time (s)', ylabel='Voltage (V)', title='C.S. Brain Wave')
plt.show()


