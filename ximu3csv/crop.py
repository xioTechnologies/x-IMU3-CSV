from dataclasses import replace
from typing import List

from .data_messages import _DataMessage
from .device import Device


def __crop(message: _DataMessage, start: int, stop: int) -> _DataMessage:
    mask = (message.timestamp >= start) & (message.timestamp <= stop)

    csv = message._csv[mask]

    string = message._string[mask] if len(message._string) > 0 else message._string

    return replace(message, _csv=csv, _string=string)


def crop(devices: List[Device], start: int = 0, stop: int = 2**64 - 1) -> List[Device]:
    return [
        Device(
            command=d.command,
            interface=d.interface,
            device_name=d.device_name,
            serial_number=d.serial_number,
            time=d.time,
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
