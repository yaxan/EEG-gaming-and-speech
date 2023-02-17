import numpy as np
from scipy.fft import fft, ifft, fftfreq
#from scipy.signal import welch

def rms_voltage_power_spectrum(time_series, min_freq, max_freq, SPS, nsamples, window=None):
    """
    Calculates the RMS voltage of a waveform between two frequency limits using Parseval's Theorem.

    :param time_series: Time series data.
    :param min_freq: Minimum frequency for which to calculate RMS voltage.
    :param max_freq: Maximum frequency for which to calculate RMS voltage.
    :param SPS: Samples per second to computer frequency 
    :param nsamples: Number of samples in original time series data.
    :param window: OPTIONAL window function to apply to time series data before FFT. If None, no window function is applied.

    :return: RMS voltage between freq_min and freq_max, ps power spectrum
    """
    #computing power spectrum
    frequencies = fftfreq(nsamples, d=1.0/SPS)
    
    #subtract the mean to ensure the time series is a zero-mean
    #Fourier assuems that time series is periodic with no DC offset
    time_series_zero_mean = time_series - np.mean(time_series)
    fourier_coeffs = fft(time_series_zero_mean)
    ps = np.abs(fourier_coeffs)**2/nsamples
    #____, ps = welch(time_series, fs=SPS)
    
    if window is not None:
        ps *= window #Apply window function to power spectrum

    freq_mask = (frequencies >= min_freq) & (frequencies <= max_freq)
    freq_range = frequencies[freq_mask]
    ps_range = ps[freq_mask]

    #Calculate RMS voltage using Parseval's Theorem
    rms = np.sqrt(np.sum(ps_range) / (nsamples * (freq_range[1] - freq_range[0])))

    return ps, rms

def gaussian_eval(relaxed, concentrated):
    """
    RETURN: threshold voltage which separates relaxed and concentrated data
    """
    
    # mean and std values for gaussian distributions
    r_mean = np.mean(relaxed)
    r_std = np.std(relaxed)
    c_mean = np.mean(concentrated)
    c_std = np.std(concentrated)

    # Solve for cross point of the two normal distributions
    a = -1/r_std**2 + 1/c_std**2
    b = 2*(-c_mean/c_std**2 + r_mean/r_std**2)
    c = c_mean**2/c_std**2 - r_mean**2/r_std**2 + np.log(c_std**2/r_std**2)
    results = np.roots([a,b,c])
    
    # Select the cross point in the middle of the two mean values.
    intersection = []
    for result in results:
        if result < r_mean and result > c_mean:
            intersection.append(result)
    
    return intersection[0]

def brain_signal_extraction(time_series, min_freq, max_freq, freq):
    """
    Extracts the components of time_series which have frequency within [min_freq, max_freq] and returns the corresponding
    brain wave signal.

    :param time_series: Numpy array containing the most recent ADC voltage difference measurements.
    :param min_freq: Minimum frequency of the desired band of brain waves.
    :param max_freq: Maximum frequency of the desired band of brain waves.
    :param freq: Array of frequencies corresponding to the power spectrum of the FFT of time_series.

    :return: Numpy array containing the extracted brain wave signal.
    """
    time_series_fft = fft(time_series)
    freq_mask = (freq >= min_freq) & (freq <= max_freq)
    time_series_fft[(~freq_mask)] = 0  #if frequency values exceed max_freq and is under min_freq, these values are set to 0
    brain_wave = ifft(time_series_fft).real
    return brain_wave
