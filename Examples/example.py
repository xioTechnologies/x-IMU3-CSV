import ximu3csv

connection = ximu3csv.read("Logged Data")[0]

print(type(connection.command))

print(type(connection.interface))
print(type(connection.serial_number))
print(type(connection.device_name))
print(type(connection.time))

print(type(connection.inertial.timestamp))
print(type(connection.inertial.gyroscope_xyz))
print(type(connection.inertial.gyroscope_x))
print(type(connection.inertial.gyroscope_y))
print(type(connection.inertial.gyroscope_z))
print(type(connection.inertial.accelerometer_xyz))
print(type(connection.inertial.accelerometer_x))
print(type(connection.inertial.accelerometer_y))
print(type(connection.inertial.accelerometer_z))

print(type(connection.magnetometer.timestamp))
print(type(connection.magnetometer.xyz))
print(type(connection.magnetometer.x))
print(type(connection.magnetometer.y))
print(type(connection.magnetometer.z))

print(type(connection.high_g_accelerometer.timestamp))
print(type(connection.high_g_accelerometer.xyz))
print(type(connection.high_g_accelerometer.x))
print(type(connection.high_g_accelerometer.y))
print(type(connection.high_g_accelerometer.z))

print(type(connection.quaternion.timestamp))
print(type(connection.quaternion.wxyz))
print(type(connection.quaternion.w))
print(type(connection.quaternion.x))
print(type(connection.quaternion.y))
print(type(connection.quaternion.z))

print(type(connection.rotation_matrix.timestamp))
print(type(connection.rotation_matrix.xx_to_zz))
print(type(connection.rotation_matrix.xx))
print(type(connection.rotation_matrix.xy))
print(type(connection.rotation_matrix.xz))
print(type(connection.rotation_matrix.yx))
print(type(connection.rotation_matrix.yy))
print(type(connection.rotation_matrix.yz))
print(type(connection.rotation_matrix.zx))
print(type(connection.rotation_matrix.zy))
print(type(connection.rotation_matrix.zz))

print(type(connection.euler_angles.timestamp))
print(type(connection.euler_angles.roll_pitch_yaw))
print(type(connection.euler_angles.roll))
print(type(connection.euler_angles.pitch))
print(type(connection.euler_angles.yaw))

print(type(connection.linear_acceleration.timestamp))
print(type(connection.linear_acceleration.xyz))
print(type(connection.linear_acceleration.x))
print(type(connection.linear_acceleration.y))
print(type(connection.linear_acceleration.z))

print(type(connection.earth_acceleration.timestamp))
print(type(connection.earth_acceleration.xyz))
print(type(connection.earth_acceleration.x))
print(type(connection.earth_acceleration.y))
print(type(connection.earth_acceleration.z))

print(type(connection.ahrs_status.timestamp))
print(type(connection.ahrs_status.string))

print(type(connection.serial_accessory.timestamp))
print(type(connection.serial_accessory.string))

print(type(connection.sync.timestamp))
print(type(connection.sync.edge))

print(type(connection.ltc.timestamp))
print(type(connection.ltc.string))

print(type(connection.temperature.timestamp))
print(type(connection.temperature.temperature))

print(type(connection.battery.timestamp))
print(type(connection.battery.percentage))
print(type(connection.battery.voltage))
print(type(connection.battery.charging_status))

print(type(connection.rssi.timestamp))
print(type(connection.rssi.percentage))
print(type(connection.rssi.power))

print(type(connection.button.timestamp))
print(type(connection.button.state))

print(type(connection.notification.timestamp))
print(type(connection.notification.string))

print(type(connection.error.timestamp))
print(type(connection.error.string))

print(type(connection.first_timestamp))
print(type(connection.last_timestamp))
