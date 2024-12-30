import sys

import ximu3csv
from matplotlib import pyplot as plt

# Filter to only read the desired data messages for faster loading
devices = ximu3csv.read(
    "Logged Data",
    filter=[
        ximu3csv.DataMessageType.INERTIAL,
        ximu3csv.DataMessageType.QUATERNION,
    ],
)

# Zero the first timestamp so that time starts at 0 microseconds
devices = ximu3csv.zero_first_timestamp(devices)

# Crop the data to include only the period of interest (between 9 and 12 seconds)
devices = ximu3csv.crop(devices, start=9e6, stop=12e6)

# Resample the data to a precise sample rate (1000 Hz)
# This also aligns the timestamp arrays across all data messages
devices = ximu3csv.resample(devices, 1000)

# Convert the list of devices into a dictionary to access by name
devices = {d.device_name: d for d in devices}

# Extract timestamps (same for all devices due to resampling)
seconds = devices["Shoulder"].inertial.timestamp / 1e6

# Plot accelerometer X axis data for each device
plt.plot(seconds, devices["Shoulder"].inertial.accelerometer.x, ".", label="Shoulder")
plt.plot(seconds, devices["Arm"].inertial.accelerometer.x, ".", label="Arm")
plt.plot(seconds, devices["Hand"].inertial.accelerometer.x, ".", label="Hand")

plt.grid()
plt.legend()

plt.show(block="dont_block" not in sys.argv)  # don't block when script run by CI
