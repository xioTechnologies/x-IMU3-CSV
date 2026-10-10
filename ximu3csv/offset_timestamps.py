from dataclasses import replace

import numpy as np

from .connection import Connection
from .data_messages import CharArrayMessage, DataMessage, FloatMessage


def zero_timestamps(connections: list[Connection]) -> list[Connection]:
    if all(c.first_timestamp is None for c in connections):
        raise ValueError("No timestamps")

    first_timestamps = [c.first_timestamp for c in connections if c.first_timestamp is not None]

    return offset_timestamps(connections, -min(first_timestamps))


def offset_timestamps(connections: list[Connection], offset: float) -> list[Connection]:
    return [
        replace(
            c,
            inertial=_offset_timestamps(c.inertial, offset),
            magnetometer=_offset_timestamps(c.magnetometer, offset),
            high_g_accelerometer=_offset_timestamps(c.high_g_accelerometer, offset),
            quaternion=_offset_timestamps(c.quaternion, offset),
            rotation_matrix=_offset_timestamps(c.rotation_matrix, offset),
            euler_angles=_offset_timestamps(c.euler_angles, offset),
            linear_acceleration=_offset_timestamps(c.linear_acceleration, offset),
            earth_acceleration=_offset_timestamps(c.earth_acceleration, offset),
            ahrs_status=_offset_timestamps(c.ahrs_status, offset),
            serial_accessory=_offset_timestamps(c.serial_accessory, offset),
            sync=_offset_timestamps(c.sync, offset),
            ltc=_offset_timestamps(c.ltc, offset),
            temperature=_offset_timestamps(c.temperature, offset),
            battery=_offset_timestamps(c.battery, offset),
            rssi=_offset_timestamps(c.rssi, offset),
            button=_offset_timestamps(c.button, offset),
            notification=_offset_timestamps(c.notification, offset),
            error=_offset_timestamps(c.error, offset),
        )
        for c in connections
    ]


def _offset_timestamps(message: DataMessage, offset: float) -> DataMessage:
    match message:
        case FloatMessage():
            return replace(message, _csv=np.column_stack((message._csv[:, 0] + offset, message._csv[:, 1:])))
        case CharArrayMessage():
            return replace(message, _timestamp=message._timestamp + offset)
