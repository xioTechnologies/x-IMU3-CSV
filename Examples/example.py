import matplotlib.pyplot as pyplot
import sys
import ximu3csv

devices = ximu3csv.import_data("Logged Data")

device = devices[0]

print("Interface: " + device.interface)
print("Serial Number: " + device.serial_number)
print("Device Name: " + device.device_name)
print("Time: " + str(device.time))

pyplot.plot(device.inertial.timestamp, device.inertial.gyroscope.x)

if len(sys.argv) == 1:  # don't show plots when script run by CI
    pyplot.show()
