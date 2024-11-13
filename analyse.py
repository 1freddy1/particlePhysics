import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def fitfunction(x, a, b):
            return a* x + b

class Calibrator():
    def __init__(self, mv, kev):
        self.mv = mv
        self.kev = kev

    def calc_fit_parameters(self):

        params, covariance = curve_fit(fitfunction, self.mv, self.kev)
        a_fit, b_fit = params
        linelist = []
        for i in range(len(self.kev)):
            linelist.append(fitfunction(self.mv[i], a_fit, b_fit))
        return a_fit, b_fit

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
    


def convert_mv_to_kev(a_fit, b_fit, mv):
        keV = []
        for i in range(len(mv)):
            keV.append(fitfunction(mv[i], a_fit, b_fit))

        return keV

def plot_results(a, b):
        plt.plot(a, b)
        plt.xlabel("keV")
        plt.ylabel("counts")


class E_error(Exception):
    pass

def calculate_delta_E(min_search, max_search, counts, kev):
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

