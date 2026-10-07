from dataclasses import replace

import numpy as np

from .data_messages import CharArrayMessage, DataMessage, FloatMessage
from .device import Device


def zero_timestamps(devices: list[Device]) -> list[Device]:
    if all(d.first_timestamp is None for d in devices):
        raise ValueError("No timestamps")

    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]

    return offset_timestamps(devices, -min(first_timestamps))


def offset_timestamps(devices: list[Device], offset: int) -> list[Device]:
    return [
        replace(
            d,
            inertial=_offset_timestamps(d.inertial, offset),
            magnetometer=_offset_timestamps(d.magnetometer, offset),
            high_g_accelerometer=_offset_timestamps(d.high_g_accelerometer, offset),
            quaternion=_offset_timestamps(d.quaternion, offset),
            rotation_matrix=_offset_timestamps(d.rotation_matrix, offset),
            euler_angles=_offset_timestamps(d.euler_angles, offset),
            linear_acceleration=_offset_timestamps(d.linear_acceleration, offset),
            earth_acceleration=_offset_timestamps(d.earth_acceleration, offset),
            ahrs_status=_offset_timestamps(d.ahrs_status, offset),
            serial_accessory=_offset_timestamps(d.serial_accessory, offset),
            sync=_offset_timestamps(d.sync, offset),
            ltc=_offset_timestamps(d.ltc, offset),
            temperature=_offset_timestamps(d.temperature, offset),
            battery=_offset_timestamps(d.battery, offset),
            rssi=_offset_timestamps(d.rssi, offset),
            button=_offset_timestamps(d.button, offset),
            notification=_offset_timestamps(d.notification, offset),
            error=_offset_timestamps(d.error, offset),
        )
        for d in devices
    ]


def _offset_timestamps(message: DataMessage, offset: int) -> DataMessage:
    match message:
        case FloatMessage():
            return replace(message, _csv=np.column_stack((message._csv[:, 0] + offset, message._csv[:, 1:])))
        case CharArrayMessage():
            return replace(message, _timestamp=message._timestamp + offset)
