## This python file contains all of the processing functions used in the jupyter notebook. 

import numpy as np 
import scipy as sp
from scipy import signal 

## Moving RMS for one channel 
def window_rms(a, window_size):
    a2 = np.power(a,2)
    window = np.ones(window_size)/float(window_size)
    return np.sqrt(np.convolve(a2, window, 'valid'))

def find_smoothRMS_1CH(a, window_size):
    a_rms = window_rms(a, window_size)
    return a_rms 

def find_smoothRMS_MultiCH(a, window_size):
    a_rms = np.zeros(a.shape)
    for i in range(a.shape[0]):
        a_rms[i,:] = window_rms(a[i,:], window_size)
    return a_rms 

def get_needle_envelope(data, cutoff, fs, filterorder):
    low_pass = cutoff/(fs/2.0)
    b3, a3 = sp.signal.butter(filterorder, low_pass, btype='lowpass')
    needle_env = sp.signal.filtfilt(b3, a3, data)
    return needle_env

def get_surface_envelope(data, cutoff, fs, filterorder):
    surface_env = np.zeros(data.shape)
    low_pass = cutoff/(fs/2.0)
    b3, a3 = sp.signal.butter(filterorder, low_pass, btype='lowpass')
    for i in range(8): 
        surface_env[i,:] = sp.signal.filtfilt(b3, a3, data[i,:])
    return surface_env 

## getting needle baseline 
def needle_baseline(data, fs, st, sp, sigma):
#     Sub_eSD = []
    baseline_env = data[fs*st:fs*sp]
    baseline_envsd1 = baseline_env.mean(axis = 0) + sigma*baseline_env.std(axis = 0)
    baseline_envsd2 = baseline_env.mean(axis = 0) - sigma*baseline_env.std(axis = 0)
    Sub_eSD = baseline_envsd1, baseline_envsd2
    return Sub_eSD

#Getting the baseline which essentially is the threshold 

def surface_baseline(data, fs, st, sp, sigma):
    Sub_eSD = np.zeros((8,2))
    for i in range(data.shape[0]):
        baseline_env = data[i,fs*st:fs*sp]
        baseline_envsd1 = baseline_env.mean(axis = 0) + sigma*baseline_env.std(axis = 0)
        baseline_envsd2 = baseline_env.mean(axis = 0) - sigma*baseline_env.std(axis = 0)
        Sub_eSD[i,:] = baseline_envsd1, baseline_envsd2
    return Sub_eSD

## Appending 0s and 1s if the data is above thresholding 

def needle_01append(data, baseline): 
    data_01 = np.zeros((data.shape))
    bl = np.mean(data, axis =0)
    for i in range(data.shape[0]): 
        d_temp = data[i]
        if d_temp < bl:
            data_01[i] = 0  
        elif d_temp >= bl:
            data_01[i] = 1
    return data_01

def surface_01append(data): 
    data_01 = np.zeros((data.shape))
    for i in range(data.shape[0]): 
        bl = np.mean(data[i,:], axis =0)
        for j in range(data.shape[1]): 
            d_temp = data[i,j]
            if d_temp < bl:
                data_01[i,j] = 0  
            elif d_temp >= bl:
                data_01[i,j] = 1
    return data_01
