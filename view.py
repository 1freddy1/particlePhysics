from analyse import Calibrator, fitfunction, find_peaks, resolution_result
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

mv = [37,101.6]
kev = [511,1274]

a_fit = 11.811145510835916
b_fit = 73.98761609907108






calibrate = Calibrator(mv, kev)
#Find the fit parameters for a line
#a_fit, b_fit = calibrate.calibrate_paramers(mv, kev)

#Read file
mV, counts = calibrate.read_spectrum('Cesium_600s')

#Smoothing out the values
counts = gaussian_filter(counts, sigma=1)

#Convert mV to keV
keV = calibrate.convert_mv_kev_list(a_fit, b_fit, mV)
max_kev = max(keV)

#Start and end keV values of the chosen peak
#This has to be a manual input. Can be automated later
start = 500
end = 2000

start_i = int(start / max_kev * 2000)
end_i = int(end / max_kev * 2000)


#Find the width of photo-peak at half maximum  
delta_E = find_peaks(start_i, end_i, counts, keV)
print(delta_E)

#Plot calibration
calibrate.plot_results(keV, counts)

#Convert 1 mV value to keV
kev = fitfunction(47 , a_fit, b_fit)

res = resolution_result(delta_E, 511)
print(f"Resolution = {res}%")


calibrated_counts_in_range = counts[0:int(2000 / max_kev * 2000)]
total_counts = sum(calibrated_counts_in_range)
print(f"Total counts = {total_counts}")

R = 5
A = 3.14 * 3 ** 2
adjusted_total_counts = total_counts * 4 * 3.14 * R ** 2 / A


print(f"Adjusted total counts = {adjusted_total_counts}")
current_activity = adjusted_total_counts / 600

adjusted_activity = current_activity / ((0.5) ** (14 / 30.17))

print(f"Activity cesium-137 = {adjusted_activity} Bq")
plt.show()

