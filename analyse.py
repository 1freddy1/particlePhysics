import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
conversion_factor = 0
def fitfunction(x, a, b):
        return a* x + b
mv = [42.6,101.6]
kev = [511,1274]
def calibrate_paramers(mv, kev):


    #plt.scatter(mv, kev)


    
    params, covariance = curve_fit(fitfunction, mv, kev)

    # Extract the fitted parameters
    a_fit, b_fit = params
    linelist = []
    for i in range(len(kev)):
        linelist.append(fitfunction(mv[i], a_fit, b_fit))

    #plt.plot(mv, linelist)
    return a_fit, b_fit

a_fit, b_fit = calibrate_paramers(mv, kev)
print(a_fit, b_fit)
def keV_conversion(a_fit, b_fit):
    mV =[]
    keV = []
    counts = []
    with open('spectrum2', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            if row == 0:
                continue
        
            mV.append(float(row[0]))
            keV.append(fitfunction(float(row[0]), a_fit, b_fit))
            counts.append(int(row[1]))

    plt.plot(keV, counts)
    plt.xlabel("keV")
    plt.ylabel("coutns")
    plt.show()


keV_conversion(a_fit, b_fit)