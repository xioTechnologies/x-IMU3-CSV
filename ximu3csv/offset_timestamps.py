from dataclasses import replace

import numpy as np

from .data_messages import CharArrayMessage, DataMessage, FloatMessage
from .logged_data import LoggedData


def zero_timestamps(data: LoggedData) -> LoggedData:
    if data.first_timestamp is None:
        raise ValueError("No timestamps")

    return offset_timestamps(data, -data.first_timestamp)


def offset_timestamps(data: LoggedData, offset: float) -> LoggedData:
    connections = tuple(
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
        for c in data
    )

    return replace(data, _connections=connections)


def _offset_timestamps(message: DataMessage, offset: float) -> DataMessage:
    match message:
        case FloatMessage():
            return replace(message, _csv=np.column_stack((message._csv[:, 0] + offset, message._csv[:, 1:])))
        case CharArrayMessage():
            return replace(message, _timestamp=message._timestamp + offset)
