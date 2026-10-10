from dataclasses import replace

import numpy as np

from .data_messages import CharArrayMessage, DataMessage, FloatMessage
from .logged_data import LoggedData


def crop(data: LoggedData, start: float | None = None, stop: float | None = None) -> LoggedData:
    if (start is None) and (stop is None):
        raise ValueError("No start or stop")

    if (start is not None) and (stop is not None) and (start > stop):
        raise ValueError(f"Start is after stop: {start} > {stop}")

    if (data.first_timestamp is None) or (data.last_timestamp is None):
        raise ValueError("No timestamps")

    if (start is not None) and (start > data.last_timestamp):
        raise ValueError(f"Start is after last timestamp: {start} > {data.last_timestamp}")

    if (stop is not None) and (stop < data.first_timestamp):
        raise ValueError(f"Stop is before first timestamp: {stop} < {data.first_timestamp}")

    connections = tuple(
        replace(
            c,
            inertial=_crop(c.inertial, start, stop),
            magnetometer=_crop(c.magnetometer, start, stop),
            high_g_accelerometer=_crop(c.high_g_accelerometer, start, stop),
            quaternion=_crop(c.quaternion, start, stop),
            rotation_matrix=_crop(c.rotation_matrix, start, stop),
            euler_angles=_crop(c.euler_angles, start, stop),
            linear_acceleration=_crop(c.linear_acceleration, start, stop),
            earth_acceleration=_crop(c.earth_acceleration, start, stop),
            ahrs_status=_crop(c.ahrs_status, start, stop),
            serial_accessory=_crop(c.serial_accessory, start, stop),
            sync=_crop(c.sync, start, stop),
            ltc=_crop(c.ltc, start, stop),
            temperature=_crop(c.temperature, start, stop),
            battery=_crop(c.battery, start, stop),
            rssi=_crop(c.rssi, start, stop),
            button=_crop(c.button, start, stop),
            notification=_crop(c.notification, start, stop),
            error=_crop(c.error, start, stop),
        )
        for c in data
    )

    return replace(data, _connections=connections)


def _crop(message: DataMessage, start: float | None, stop: float | None) -> DataMessage:
    mask = np.full(len(message.timestamp), True)

    if start is not None:
        mask &= message.timestamp >= start

    if stop is not None:
        mask &= message.timestamp <= stop

    match message:
        case FloatMessage():
            return replace(message, _csv=message._csv[mask])
        case CharArrayMessage():
            return replace(message, _timestamp=message._timestamp[mask], _string=message._string[mask])
