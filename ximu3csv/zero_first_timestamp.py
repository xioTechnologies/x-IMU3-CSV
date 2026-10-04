from dataclasses import replace

from .device import Device


def zero_first_timestamp(devices: list[Device]) -> list[Device]:
    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]

    if not first_timestamps:
        return devices

    offset = -min(first_timestamps)

    return [
        replace(
            d,
            inertial=d.inertial._offset_timestamp(offset),
            magnetometer=d.magnetometer._offset_timestamp(offset),
            high_g_accelerometer=d.high_g_accelerometer._offset_timestamp(offset),
            quaternion=d.quaternion._offset_timestamp(offset),
            rotation_matrix=d.rotation_matrix._offset_timestamp(offset),
            euler_angles=d.euler_angles._offset_timestamp(offset),
            linear_acceleration=d.linear_acceleration._offset_timestamp(offset),
            earth_acceleration=d.earth_acceleration._offset_timestamp(offset),
            ahrs_status=d.ahrs_status._offset_timestamp(offset),
            serial_accessory=d.serial_accessory._offset_timestamp(offset),
            sync=d.sync._offset_timestamp(offset),
            ltc=d.ltc._offset_timestamp(offset),
            temperature=d.temperature._offset_timestamp(offset),
            battery=d.battery._offset_timestamp(offset),
            rssi=d.rssi._offset_timestamp(offset),
            button=d.button._offset_timestamp(offset),
            notification=d.notification._offset_timestamp(offset),
            error=d.error._offset_timestamp(offset),
        )
        for d in devices
    ]
