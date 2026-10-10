from collections.abc import Sequence
from dataclasses import replace

import numpy as np

from ..connection import Connection, max_last_timestamp, min_first_timestamp
from ..data_messages import CharArrayMessage, DataMessage, FloatMessage


def crop(connections: Sequence[Connection], start: float | None, stop: float | None) -> tuple[Connection, ...]:
    if (start is None) and (stop is None):
        raise ValueError("No start or stop")

    if (start is not None) and (stop is not None) and (start > stop):
        raise ValueError(f"Start is after stop: {start} > {stop}")

    first_timestamp = min_first_timestamp(connections)
    last_timestamp = max_last_timestamp(connections)

    if (first_timestamp is None) or (last_timestamp is None):
        raise ValueError("No timestamps")

    if (start is not None) and (start > last_timestamp):
        raise ValueError(f"Start is after last timestamp: {start} > {last_timestamp}")

    if (stop is not None) and (stop < first_timestamp):
        raise ValueError(f"Stop is before first timestamp: {stop} < {first_timestamp}")

    return tuple(
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
        for c in connections
    )


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
