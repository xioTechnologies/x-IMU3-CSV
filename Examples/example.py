import ximu3csv

device = ximu3csv.read("Logged Data")[0]

print(type(device.command))

print(type(device.interface))
print(type(device.serial_number))
print(type(device.device_name))
print(type(device.time))

print(type(device.inertial.timestamp))
print(type(device.inertial.gyroscope.xyz))
print(type(device.inertial.gyroscope.x))
print(type(device.inertial.gyroscope.y))
print(type(device.inertial.gyroscope.z))
print(type(device.inertial.accelerometer.xyz))
print(type(device.inertial.accelerometer.x))
print(type(device.inertial.accelerometer.y))
print(type(device.inertial.accelerometer.z))

print(type(device.magnetometer.timestamp))
print(type(device.magnetometer.magnetometer.xyz))
print(type(device.magnetometer.magnetometer.x))
print(type(device.magnetometer.magnetometer.y))
print(type(device.magnetometer.magnetometer.z))

print(type(device.quaternion.timestamp))
print(type(device.quaternion.quaternion.wxyz))
print(type(device.quaternion.quaternion.w))
print(type(device.quaternion.quaternion.x))
print(type(device.quaternion.quaternion.y))
print(type(device.quaternion.quaternion.z))

print(type(device.rotation_matrix.timestamp))
print(type(device.rotation_matrix.rotation_matrix))
print(type(device.rotation_matrix.xy))
print(type(device.rotation_matrix.xy))
print(type(device.rotation_matrix.xz))
print(type(device.rotation_matrix.yy))
print(type(device.rotation_matrix.yy))
print(type(device.rotation_matrix.yz))
print(type(device.rotation_matrix.zy))
print(type(device.rotation_matrix.zy))
print(type(device.rotation_matrix.zz))

print(type(device.euler_angles.timestamp))
print(type(device.euler_angles.euler_angles))
print(type(device.euler_angles.roll))
print(type(device.euler_angles.pitch))
print(type(device.euler_angles.yaw))

print(type(device.linear_acceleration.timestamp))
print(type(device.linear_acceleration.linear_acceleration.xyz))
print(type(device.linear_acceleration.linear_acceleration.x))
print(type(device.linear_acceleration.linear_acceleration.x))
print(type(device.linear_acceleration.linear_acceleration.y))
print(type(device.linear_acceleration.quaternion.wxyz))
print(type(device.linear_acceleration.quaternion.w))
print(type(device.linear_acceleration.quaternion.x))
print(type(device.linear_acceleration.quaternion.y))
print(type(device.linear_acceleration.quaternion.z))

print(type(device.earth_acceleration.timestamp))
print(type(device.earth_acceleration.earth_acceleration.xyz))
print(type(device.earth_acceleration.earth_acceleration.x))
print(type(device.earth_acceleration.earth_acceleration.x))
print(type(device.earth_acceleration.earth_acceleration.y))
print(type(device.earth_acceleration.quaternion.wxyz))
print(type(device.earth_acceleration.quaternion.w))
print(type(device.earth_acceleration.quaternion.x))
print(type(device.earth_acceleration.quaternion.y))
print(type(device.earth_acceleration.quaternion.z))

print(type(device.ahrs_status.timestamp))
print(type(device.ahrs_status.initialising))
print(type(device.ahrs_status.angular_rate_recovery))
print(type(device.ahrs_status.acceleration_rate_recovery))
print(type(device.ahrs_status.magnetic_rate_recovery))

print(type(device.high_g_accelerometer.timestamp))
print(type(device.high_g_accelerometer.high_g_accelerometer.xyz))
print(type(device.high_g_accelerometer.high_g_accelerometer.x))
print(type(device.high_g_accelerometer.high_g_accelerometer.y))
print(type(device.high_g_accelerometer.high_g_accelerometer.z))

print(type(device.temperature.timestamp))
print(type(device.temperature.temperature))

print(type(device.battery.timestamp))
print(type(device.battery.percentage))
print(type(device.battery.voltage))
print(type(device.battery.charging_status))

print(type(device.rssi.timestamp))
print(type(device.rssi.percentage))
print(type(device.rssi.power))

print(type(device.serial_accessory.timestamp))
print(type(device.serial_accessory.csv))

print(type(device.notification.timestamp))
print(type(device.notification.string))

print(type(device.error.timestamp))
print(type(device.error.string))

print(type(device.first_timestamp))
print(type(device.last_timestamp))
