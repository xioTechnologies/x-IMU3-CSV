from collections.abc import Sequence
from dataclasses import replace

import numpy as np

from ..connection import Connection, max_last_timestamp, min_first_timestamp
from ..data_messages import CharArrayMessage, DataMessage, FloatMessage


def truncate(connections: Sequence[Connection], before: float | None, after: float | None) -> tuple[Connection, ...]:
    if (before is None) and (after is None):
        raise ValueError("No before or after")

    if (before is not None) and (after is not None) and (before > after):
        raise ValueError(f"Before is greater than after: {before} > {after}")

    first_timestamp = min_first_timestamp(connections)
    last_timestamp = max_last_timestamp(connections)

    if (first_timestamp is None) or (last_timestamp is None):
        raise ValueError("No timestamps")

    if (before is not None) and (before > last_timestamp):
        raise ValueError(f"Before is greater than last timestamp: {before} > {last_timestamp}")

    if (after is not None) and (after < first_timestamp):
        raise ValueError(f"After is less than first timestamp: {after} < {first_timestamp}")

    return tuple(
        replace(
            c,
            inertial=_truncate(c.inertial, before, after),
            magnetometer=_truncate(c.magnetometer, before, after),
            high_g_accelerometer=_truncate(c.high_g_accelerometer, before, after),
            quaternion=_truncate(c.quaternion, before, after),
            rotation_matrix=_truncate(c.rotation_matrix, before, after),
            euler_angles=_truncate(c.euler_angles, before, after),
            linear_acceleration=_truncate(c.linear_acceleration, before, after),
            earth_acceleration=_truncate(c.earth_acceleration, before, after),
            ahrs_status=_truncate(c.ahrs_status, before, after),
            serial_accessory=_truncate(c.serial_accessory, before, after),
            sync=_truncate(c.sync, before, after),
            ltc=_truncate(c.ltc, before, after),
            temperature=_truncate(c.temperature, before, after),
            battery=_truncate(c.battery, before, after),
            rssi=_truncate(c.rssi, before, after),
            button=_truncate(c.button, before, after),
            notification=_truncate(c.notification, before, after),
            error=_truncate(c.error, before, after),
        )
        for c in connections
    )


def _truncate(message: DataMessage, before: float | None, after: float | None) -> DataMessage:
    mask = np.full(len(message.timestamp), True)

    if before is not None:
        mask &= message.timestamp >= before

    if after is not None:
        mask &= message.timestamp <= after

    match message:
        case FloatMessage():
            return replace(message, _csv=message._csv[mask])
        case CharArrayMessage():
            return replace(message, _timestamp=message._timestamp[mask], _string=message._string[mask])
