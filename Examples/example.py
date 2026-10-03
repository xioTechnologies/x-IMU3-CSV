import ximu3csv

device = ximu3csv.read("Logged Data")[0]

print(type(device.command))

print(type(device.interface))
print(type(device.serial_number))
print(type(device.device_name))
print(type(device.time))

print(type(device.inertial.timestamp))
print(type(device.inertial.gyroscope_xyz))
print(type(device.inertial.gyroscope_x))
print(type(device.inertial.gyroscope_y))
print(type(device.inertial.gyroscope_z))
print(type(device.inertial.accelerometer_xyz))
print(type(device.inertial.accelerometer_x))
print(type(device.inertial.accelerometer_y))
print(type(device.inertial.accelerometer_z))

print(type(device.magnetometer.timestamp))
print(type(device.magnetometer.xyz))
print(type(device.magnetometer.x))
print(type(device.magnetometer.y))
print(type(device.magnetometer.z))

print(type(device.high_g_accelerometer.timestamp))
print(type(device.high_g_accelerometer.xyz))
print(type(device.high_g_accelerometer.x))
print(type(device.high_g_accelerometer.y))
print(type(device.high_g_accelerometer.z))

print(type(device.quaternion.timestamp))
print(type(device.quaternion.wxyz))
print(type(device.quaternion.w))
print(type(device.quaternion.x))
print(type(device.quaternion.y))
print(type(device.quaternion.z))

print(type(device.rotation_matrix.timestamp))
print(type(device.rotation_matrix.xx_to_zz))
print(type(device.rotation_matrix.xx))
print(type(device.rotation_matrix.xy))
print(type(device.rotation_matrix.xz))
print(type(device.rotation_matrix.yx))
print(type(device.rotation_matrix.yy))
print(type(device.rotation_matrix.yz))
print(type(device.rotation_matrix.zx))
print(type(device.rotation_matrix.zy))
print(type(device.rotation_matrix.zz))

print(type(device.euler_angles.timestamp))
print(type(device.euler_angles.roll_pitch_yaw))
print(type(device.euler_angles.roll))
print(type(device.euler_angles.pitch))
print(type(device.euler_angles.yaw))

print(type(device.linear_acceleration.timestamp))
print(type(device.linear_acceleration.xyz))
print(type(device.linear_acceleration.x))
print(type(device.linear_acceleration.y))
print(type(device.linear_acceleration.z))

print(type(device.earth_acceleration.timestamp))
print(type(device.earth_acceleration.xyz))
print(type(device.earth_acceleration.x))
print(type(device.earth_acceleration.y))
print(type(device.earth_acceleration.z))

print(type(device.ahrs_status.timestamp))
print(type(device.ahrs_status.string))

print(type(device.serial_accessory.timestamp))
print(type(device.serial_accessory.csv))

print(type(device.sync.timestamp))
print(type(device.sync.edge))

print(type(device.ltc.timestamp))
print(type(device.ltc.string))

print(type(device.temperature.timestamp))
print(type(device.temperature.temperature))

print(type(device.battery.timestamp))
print(type(device.battery.percentage))
print(type(device.battery.voltage))
print(type(device.battery.charging_status))

print(type(device.rssi.timestamp))
print(type(device.rssi.percentage))
print(type(device.rssi.power))

print(type(device.button.timestamp))
print(type(device.button.state))

print(type(device.notification.timestamp))
print(type(device.notification.string))

print(type(device.error.timestamp))
print(type(device.error.string))

print(type(device.first_timestamp))
print(type(device.last_timestamp))
