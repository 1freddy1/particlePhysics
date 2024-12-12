import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import lmfit
def fitfunction(x, a, b):
            return a* x + b

def reverse(y, a, b):
    return (y - b) /a
class Calibrator():
    def __init__(self, mv, kev):
        self.mv = mv
        self.kev = kev

    def calibrate(self, mv, kev, mv_err):
        model = lmfit.Model(fitfunction)

        # Create parameters for the model (initial guesses for a and b)
        params = model.make_params(a=1, b=0)
        mv_err = np.array(mv_err)
        result = model.fit(kev, params, x=mv, weights=1/mv_err)
        print(result.fit_report())
        return result

    def calibrate_paramers(self, mv, kev, mv_err):

        params, covariance = curve_fit(fitfunction, mv, kev)
        a_fit, b_fit = params
        linelist = []
        for i in range(len(kev)):
            linelist.append(fitfunction(mv[i], a_fit, b_fit))
        return a_fit, b_fit
    def convert_mv_kev_list(self, a_fit, b_fit, mv):
        keV = []
        for i in range(len(mv)):
            
            keV.append(fitfunction(mv[i], a_fit, b_fit))
        return keV

    def read_spectrum(self, file, two=False):
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

    def read_csv(self, file):
        mV =[]
        counts = []
        with open(file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                mV.append(float(row[0]))
                counts.append(int(row[1]))
        return mV, counts
    
    def plot_results(self, a, b):
        plt.plot(a, b)
        plt.xlabel("keV")
        plt.ylabel("coutns")

        
mv = [42.6,101.6]
kev = [511,1274]

def create_mv_kev_list(a_fit, b_fit, file):
    mV =[]
    keV = []
    counts = []
    with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            mV.append(float(row[0]))
            keV.append(fitfunction(float(row[0]), a_fit, b_fit))
            counts.append(int(row[1]))
class E_error(Exception):
    pass
def find_peaks(min_search, max_search, counts, kev):
    delta_E = []
    new_count_list = counts[min_search:max_search]
    new_kev_list = kev[min_search:max_search]
    top_count = max(new_count_list)
    half_count = top_count / 2
    for i in range(len(new_count_list)- 1):
        y1 = new_count_list[i]
        y2 = new_count_list[i+1]
        x1 = new_kev_list[i]
        x2 = new_kev_list[i+1]
        a = (y2-y1) / (x2-x1)
        b = y1 - a * x1
        y_max = a * x2 + b
        y_min = a * x1 + b
        if a > 0:
            if half_count >= y_min and half_count <= y_max:
                delta_E.append(kev[i])
        else:
            if half_count <= y_min and half_count >= y_max:
                delta_E.append(kev[i])
    if len(delta_E)>2:
        raise E_error("delta_E list is too long!")
    return delta_E[1] - delta_E[0]

def resolution_result(delta_E, E):
    return delta_E / E * 100

