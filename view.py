from analyse import Calibrator, fitfunction, find_peaks, resolution_result, reverse
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import lmfit
mv = [37,89]
kev = [511,1274]
mv_err = [1, 1]

a_fit = 14.673076923076923
b_fit = -31.90384615384616



new_a = 1/a_fit
new_b = -b_fit/a_fit
print(new_a)
print(new_b)


calibrate = Calibrator(mv, kev)

#Find the fit parameters for a line
a_fit, b_fit = calibrate.calibrate_paramers(mv, kev, mv_err)




#Read file
mV, counts = calibrate.read_spectrum('cobalt')
plt.plot(mV, counts)
plt.show()
#Smoothing out the values
counts = gaussian_filter(counts, sigma=2)

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
#delta_E = find_peaks(start_i, end_i, counts, keV)
#print(f"delta_E = {delta_E}")

#Plot calibration
calibrate.plot_results(keV, counts)

#Convert a mV value to keV
kev = reverse(1330 , a_fit, b_fit)
print(f"Value of 2nd cobalt peak is at {kev}")









# res = resolution_result(delta_E, 511)
# print(f"Resolution = {res}%")


# calibrated_counts_in_range = counts[0:int(2000 / max_kev * 2000)]
# total_counts = sum(calibrated_counts_in_range)
# print(f"Total counts = {total_counts}")

# R = 5
# A = 3.14 * 3 ** 2
# adjusted_total_counts = total_counts * 4 * 3.14 * R ** 2 / A


# print(f"Adjusted total counts = {adjusted_total_counts}")
# current_activity = adjusted_total_counts / 600

# adjusted_activity = current_activity / ((0.5) ** (14 / 30.17))

# print(f"Activity cesium-137 = {adjusted_activity} Bq")


