import sys

import matplotlib.pyplot as plt
import ximu3csv

# Read data
devices = ximu3csv.read("Logged Data")

# Select first device in list
device = devices[0]

# Inertial
figure, axes = plt.subplots(nrows=2, sharex=True)

figure.suptitle("Inertial")

axes[0].plot(device.inertial.timestamp, device.inertial.gyroscope.x, "tab:red", label="X")
axes[0].plot(device.inertial.timestamp, device.inertial.gyroscope.y, "tab:green", label="Y")
axes[0].plot(device.inertial.timestamp, device.inertial.gyroscope.z, "tab:blue", label="Z")
axes[0].set_title("Gyroscope")
axes[0].set_ylabel("deg/s")
axes[0].grid()
axes[0].legend()

axes[1].plot(device.inertial.timestamp, device.inertial.accelerometer.x, "tab:red", label="X")
axes[1].plot(device.inertial.timestamp, device.inertial.accelerometer.y, "tab:green", label="Y")
axes[1].plot(device.inertial.timestamp, device.inertial.accelerometer.z, "tab:blue", label="Z")
axes[1].set_title("Accelerometer")
axes[1].set_ylabel("g")
axes[1].grid()
axes[1].legend()

axes[1].set_xlabel("us")

# Magnetometer
plt.figure()
plt.plot(device.magnetometer.timestamp, device.magnetometer.magnetometer.x, "tab:red", label="X")
plt.plot(device.magnetometer.timestamp, device.magnetometer.magnetometer.y, "tab:green", label="Y")
plt.plot(device.magnetometer.timestamp, device.magnetometer.magnetometer.z, "tab:blue", label="Z")
plt.title("Magnetometer")
plt.xlabel("us")
plt.ylabel("a.u.")
plt.grid()
plt.legend()

# Quaternion
plt.figure()
plt.plot(device.quaternion.timestamp, device.quaternion.quaternion.w, "tab:gray", label="W")
plt.plot(device.quaternion.timestamp, device.quaternion.quaternion.x, "tab:red", label="X")
plt.plot(device.quaternion.timestamp, device.quaternion.quaternion.y, "tab:green", label="Y")
plt.plot(device.quaternion.timestamp, device.quaternion.quaternion.z, "tab:blue", label="Z")
plt.title("Quaternion")
plt.xlabel("us")
plt.grid()
plt.legend()

# Rotation matrix
plt.figure()
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.xx, label="XX")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.xy, label="XY")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.xz, label="XZ")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.yx, label="YX")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.yy, label="YY")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.yz, label="YZ")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.zx, label="ZX")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.zy, label="ZY")
plt.plot(device.rotation_matrix.timestamp, device.rotation_matrix.zz, label="ZZ")
plt.title("Rotation matrix")
plt.xlabel("us")
plt.grid()
plt.legend()

# Euler angles
plt.figure()
plt.plot(device.euler_angles.timestamp, device.euler_angles.roll, "tab:red", label="Roll")
plt.plot(device.euler_angles.timestamp, device.euler_angles.pitch, "tab:green", label="Pitch")
plt.plot(device.euler_angles.timestamp, device.euler_angles.yaw, "tab:blue", label="Yaw")
plt.title("Euler angles")
plt.xlabel("us")
plt.ylabel("deg")
plt.grid()
plt.legend()

# Linear acceleration
figure, axes = plt.subplots(nrows=2, sharex=True)

figure.suptitle("Linear acceleration")

axes[0].plot(device.linear_acceleration.timestamp, device.linear_acceleration.linear_acceleration.x, "tab:red", label="X")
axes[0].plot(device.linear_acceleration.timestamp, device.linear_acceleration.linear_acceleration.y, "tab:green", label="Y")
axes[0].plot(device.linear_acceleration.timestamp, device.linear_acceleration.linear_acceleration.z, "tab:blue", label="Z")
axes[0].set_title("Linear acceleration")
axes[0].set_ylabel("g")
axes[0].grid()
axes[0].legend()

axes[1].plot(device.linear_acceleration.timestamp, device.linear_acceleration.quaternion.w, "tab:gray", label="W")
axes[1].plot(device.linear_acceleration.timestamp, device.linear_acceleration.quaternion.x, "tab:red", label="X")
axes[1].plot(device.linear_acceleration.timestamp, device.linear_acceleration.quaternion.y, "tab:green", label="Y")
axes[1].plot(device.linear_acceleration.timestamp, device.linear_acceleration.quaternion.z, "tab:blue", label="Z")
axes[1].set_title("Quaternion")
axes[1].grid()
axes[1].legend()

axes[1].set_xlabel("us")

# Earth acceleration
figure, axes = plt.subplots(nrows=2, sharex=True)

figure.suptitle("Earth acceleration")

axes[0].plot(device.earth_acceleration.timestamp, device.earth_acceleration.earth_acceleration.x, "tab:red", label="X")
axes[0].plot(device.earth_acceleration.timestamp, device.earth_acceleration.earth_acceleration.y, "tab:green", label="Y")
axes[0].plot(device.earth_acceleration.timestamp, device.earth_acceleration.earth_acceleration.z, "tab:blue", label="Z")
axes[0].set_title("Earth acceleration")
axes[0].set_ylabel("g")
axes[0].grid()
axes[0].legend()

axes[1].plot(device.earth_acceleration.timestamp, device.earth_acceleration.quaternion.w, "tab:gray", label="W")
axes[1].plot(device.earth_acceleration.timestamp, device.earth_acceleration.quaternion.x, "tab:red", label="X")
axes[1].plot(device.earth_acceleration.timestamp, device.earth_acceleration.quaternion.y, "tab:green", label="Y")
axes[1].plot(device.earth_acceleration.timestamp, device.earth_acceleration.quaternion.z, "tab:blue", label="Z")
axes[1].set_title("Quaternion")
axes[1].grid()
axes[1].legend()

axes[1].set_xlabel("us")

# AHRS status
figure, axes = plt.subplots(nrows=4, sharex=True)

figure.suptitle("AHRS status")

axes[0].plot(device.ahrs_status.timestamp, device.ahrs_status.initialising)
axes[0].set_title("Initialising")
axes[0].grid()
plt.sca(axes[0])
plt.yticks([0, 1], ["False", "True"])

axes[1].plot(device.ahrs_status.timestamp, device.ahrs_status.angular_rate_recovery)
axes[1].set_title("Angular rate recovery")
axes[1].grid()
plt.sca(axes[1])
plt.yticks([0, 1], ["False", "True"])

axes[2].plot(device.ahrs_status.timestamp, device.ahrs_status.acceleration_rate_recovery)
axes[2].set_title("Acceleration rate recovery")
axes[2].grid()
plt.sca(axes[2])
plt.yticks([0, 1], ["False", "True"])

axes[3].plot(device.ahrs_status.timestamp, device.ahrs_status.magnetic_rate_recovery)
axes[3].set_title("Magnetic rate recovery")
axes[3].grid()
plt.sca(axes[3])
plt.yticks([0, 1], ["False", "True"])

axes[3].set_xlabel("us")

# High-g accelerometer
plt.figure()
plt.plot(device.high_g_accelerometer.timestamp, device.high_g_accelerometer.high_g_accelerometer.x, "tab:red", label="X")
plt.plot(device.high_g_accelerometer.timestamp, device.high_g_accelerometer.high_g_accelerometer.y, "tab:green", label="Y")
plt.plot(device.high_g_accelerometer.timestamp, device.high_g_accelerometer.high_g_accelerometer.z, "tab:blue", label="Z")
plt.title("High-g accelerometer")
plt.xlabel("us")
plt.ylabel("g")
plt.grid()
plt.legend()

# Temperature
plt.figure()
plt.plot(device.temperature.timestamp, device.temperature.temperature)
plt.title("Temperature")
plt.xlabel("us")
plt.ylabel("Degrees Celsius")
plt.grid()

# Battery
figure, axes = plt.subplots(nrows=3, sharex=True)

figure.suptitle("Battery")

axes[0].plot(device.battery.timestamp, device.battery.percentage)
axes[0].set_title("Percentage")
axes[0].set_ylabel("%")
axes[0].grid()

axes[1].plot(device.battery.timestamp, device.battery.voltage)
axes[1].set_title("Voltage")
axes[1].set_ylabel("V")
axes[1].grid()

axes[2].plot(device.battery.timestamp, device.battery.charging_status)
axes[2].set_title("Charging status")
axes[2].grid()
plt.sca(axes[2])
plt.yticks([0, 1, 2], ["Not connected", "Charging", "Charging complete"])

axes[2].set_xlabel("us")

# RSSI
figure, axes = plt.subplots(nrows=2, sharex=True)

figure.suptitle("RSSI")

axes[0].plot(device.rssi.timestamp, device.rssi.percentage)
axes[0].set_title("Percentage")
axes[0].set_ylabel("%")
axes[0].grid()

axes[1].plot(device.rssi.timestamp, device.rssi.power)
axes[1].set_title("Power")
axes[1].set_ylabel("dBm")
axes[1].grid()

axes[1].set_xlabel("us")

# Serial accessory (x-IMU3-SA-A8)
plt.figure()
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 0], label="Channel 1")
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 1], label="Channel 2")
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 2], label="Channel 3")
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 3], label="Channel 4")
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 4], label="Channel 5")
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 5], label="Channel 6")
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 6], label="Channel 7")
plt.plot(device.serial_accessory.timestamp, device.serial_accessory.csv[:, 7], label="Channel 8")
plt.title("Serial accessory (x-IMU3-SA-A8)")
plt.xlabel("us")
plt.ylabel("V")
plt.grid()
plt.legend()

# Notification
for timestamp, string in zip(device.notification.timestamp, device.notification.string):
    print(f"Notification {timestamp} us {string}")

# Error
for timestamp, string in zip(device.error.timestamp, device.error.string):
    print(f"Error {timestamp} us {string}")

plt.show(block="dont_block" not in sys.argv)  # don't block when script run by CI
