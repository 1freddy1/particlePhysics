from analyse import Calibrator, fitfunction, convert_mv_to_kev, plot_results, calculate_delta_E, resolution_result
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


#Original data from spectrums
start_mv = [37,101.6]
start_kev = [511,1274]



calibrator = Calibrator(start_mv, start_kev)
#Find the fit parameters for a line

a_fit, b_fit = calibrator.calc_fit_parameters()

#Read file
mV, counts = calibrator.read_csv('Cesium_600s')

#Smoothing out the values
counts = gaussian_filter(counts, sigma=1)

#Convert mV to keV
keV = convert_mv_to_kev(a_fit, b_fit, mV)

max_kev = max(keV)

#Start and end keV values of the chosen peak
#This has to be a manual input. Can be automated later
start = 500
end = 2000

start_i = int(start / max_kev * 2000)
end_i = int(end / max_kev * 2000)


#Find the width of photo-peak at half maximum  
delta_E = calculate_delta_E(start_i, end_i, counts, keV)
print(f"Delta_E = {delta_E}")

#Plot calibration
plot_results(keV, counts)

#Calculate resolution of the detector
res = resolution_result(delta_E, 511)
print(f"Resolution = {res}%")

#Count only gamma rays up until 2000keV
counts_in_range = counts[0:int(2000 / max_kev * 2000)]
total_counts = sum(counts_in_range)
print(f"Total counts = {total_counts}")

#Because we only measure the gamma rays on a small surface we have to account for
#gamma-rays going in other directions
R = 5
A = 3.14 * 3 ** 2
adjusted_total_counts = total_counts * 4 * 3.14 * R ** 2 / A
print(f"Adjusted total counts = {adjusted_total_counts}")

#Calculate activity when the material was created

half_life = 30.17 #Years
time_since_creation = 14 #Years
measurement_time = 600 #Seconds

current_activity = adjusted_total_counts / measurement_time
adjusted_activity = current_activity / ((0.5) ** (time_since_creation / half_life))
print(f"Activity cesium-137 = {adjusted_activity} Bq")

plt.show()

