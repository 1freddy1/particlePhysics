from analyse import Calibrator, fitfunction, find_peaks, resolution_result, reverse
import csv
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np

def read_spectrum(file, two=False):
        if two == False:
            mV =[]
            counts = []
            with open(file, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                for row in csvreader:
                    mV.append(float(row[0]))
                    counts.append(int(row[1]))
        
            return mV, counts
        if two == True:
            mV =[]
            count_a = []
            count_b = []
            with open(file, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                for row in csvreader:
                    mV.append(float(row[0]))
                    count_a.append(int(row[1]))
                    count_b.append(int(row[2]))
            return mV, count_a, count_b

    

mV, count_a, count_b = read_spectrum('spectrum.csv', True)
plt.plot(count_a)
#plt.show()

def calc_peak(counts):
    counts = counts[170:]
    counts = gaussian_filter(counts, sigma=2)
    peak = max(counts)
    return peak

peak_1 = calc_peak(count_a)
peak_2 = calc_peak(count_b)



peak_1_std = np.sqrt(peak_1)
peak_2_std = np.sqrt(peak_2)

def First_part(x, L, p_1, p_2):
    return -(L / (1+np.sqrt(p_1 / p_2)) ** 2) * 0.5 * (1 / p_2) * (1/ np.sqrt(p_1))

def Second_part(x, L, p_1, p_2):
    return L  / ((1+ np.sqrt(p_1 / p_2))**2) * 0.5 * (p_1 / (p_2 ** (3/2)))

def Third_part(p_1, p_2):
    return 1 / (1+np.sqrt(p_1 / p_2))




L = 28.5
L_err = 0.01
x = 1 / (1 + np.sqrt(peak_1 / peak_2))
x_err = np.sqrt((First_part(x,L,peak_1,peak_2) * peak_1_std) ** 2 + (Second_part(x,L,peak_1,peak_2) * peak_2_std) ** 2 + (Third_part(peak_1, peak_2) * L_err)**2)
print(x_err)

print(f"Distance from right detector = {x * L}")