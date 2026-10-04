from dataclasses import replace

from .device import Device


def crop(devices: list[Device], start: int = 0, stop: int = 2**64 - 1) -> list[Device]:
    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]
    last_timestamps = [d.last_timestamp for d in devices if d.last_timestamp is not None]

    if not first_timestamps or not last_timestamps:
        return devices

    if start > max(last_timestamps):
        raise ValueError(f"Start is after last timestamp: {start} > {max(last_timestamps)}")

    if stop < min(first_timestamps):
        raise ValueError(f"Stop is before first timestamp: {stop} < {min(first_timestamps)}")

    return [
        replace(
            d,
            inertial=d.inertial._crop(start, stop),
            magnetometer=d.magnetometer._crop(start, stop),
            high_g_accelerometer=d.high_g_accelerometer._crop(start, stop),
            quaternion=d.quaternion._crop(start, stop),
            rotation_matrix=d.rotation_matrix._crop(start, stop),
            euler_angles=d.euler_angles._crop(start, stop),
            linear_acceleration=d.linear_acceleration._crop(start, stop),
            earth_acceleration=d.earth_acceleration._crop(start, stop),
            ahrs_status=d.ahrs_status._crop(start, stop),
            serial_accessory=d.serial_accessory._crop(start, stop),
            sync=d.sync._crop(start, stop),
            ltc=d.ltc._crop(start, stop),
            temperature=d.temperature._crop(start, stop),
            battery=d.battery._crop(start, stop),
            rssi=d.rssi._crop(start, stop),
            button=d.button._crop(start, stop),
            notification=d.notification._crop(start, stop),
            error=d.error._crop(start, stop),
        )
        for d in devices
    ]
