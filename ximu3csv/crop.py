from dataclasses import replace
from typing import List

from .data_messages import DataMessage
from .device import Device, update_first_and_last_timestamps


def __crop(message: DataMessage, start: int, stop: int) -> DataMessage:
    mask = (message.timestamp >= start) & (message.timestamp <= stop)

    return replace(
        message,
        _csv=message._csv[mask],
        _string=message._string[mask] if len(message._string) > 0 else message._string,
    )


def crop(devices: List[Device], start: int = 0, stop: int = 2**64 - 1) -> List[Device]:
    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]
    last_timestamps = [d.last_timestamp for d in devices if d.last_timestamp is not None]

    if not first_timestamps or not last_timestamps:
        return devices

    if start > max(last_timestamps):
        raise ValueError(f"Start {start} is after last timestamp {max(last_timestamps)}")

    if stop < min(first_timestamps):
        raise ValueError(f"Stop {stop} is before first timestamp {min(first_timestamps)}")

    devices = [
        replace(
            d,
            inertial=__crop(d.inertial, start, stop),
            magnetometer=__crop(d.magnetometer, start, stop),
            quaternion=__crop(d.quaternion, start, stop),
            rotation_matrix=__crop(d.rotation_matrix, start, stop),
            euler_angles=__crop(d.euler_angles, start, stop),
            linear_acceleration=__crop(d.linear_acceleration, start, stop),
            earth_acceleration=__crop(d.earth_acceleration, start, stop),
            ahrs_status=__crop(d.ahrs_status, start, stop),
            high_g_accelerometer=__crop(d.high_g_accelerometer, start, stop),
            temperature=__crop(d.temperature, start, stop),
            battery=__crop(d.battery, start, stop),
            rssi=__crop(d.rssi, start, stop),
            serial_accessory=__crop(d.serial_accessory, start, stop),
            notification=__crop(d.notification, start, stop),
            error=__crop(d.error, start, stop),
        )
        for d in devices
    ]

    return [update_first_and_last_timestamps(d) for d in devices]
