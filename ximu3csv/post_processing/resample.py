from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection
from ..data_messages import FloatMessage, OrientationMessage


def resample(connections: Sequence[Connection], sample_rate: float) -> tuple[Connection, ...]:
    if sample_rate <= 0:
        raise ValueError(f"Invalid sample rate: {sample_rate}")

    if all(c.first_timestamp is None for c in connections):
        raise ValueError("No timestamps")

    first_timestamps = [c.first_timestamp for c in connections if c.first_timestamp is not None]
    last_timestamps = [c.last_timestamp for c in connections if c.last_timestamp is not None]

    first_timestamp = max(first_timestamps)
    last_timestamp = min(last_timestamps)

    if first_timestamp >= last_timestamp:
        raise ValueError(f"No overlapping timestamps: {first_timestamp} >= {last_timestamp}")

    timestamp = np.arange(first_timestamp, last_timestamp, 1e6 / sample_rate)

    return tuple(
        replace(
            c,
            inertial=_resample(c.inertial, timestamp),
            magnetometer=_resample(c.magnetometer, timestamp),
            high_g_accelerometer=_resample(c.high_g_accelerometer, timestamp),
            quaternion=_resample(c.quaternion, timestamp),
            rotation_matrix=_resample(c.rotation_matrix, timestamp),
            euler_angles=_resample(c.euler_angles, timestamp),
            linear_acceleration=_resample(c.linear_acceleration, timestamp),
            earth_acceleration=_resample(c.earth_acceleration, timestamp),
            sync=_resample(c.sync, timestamp),  # TODO: Do not interpolate edges
            temperature=_resample(c.temperature, timestamp),
            battery=_resample(c.battery, timestamp),
            rssi=_resample(c.rssi, timestamp),
            button=_resample(c.button, timestamp),  # TODO: Do not interpolate edges
        )
        for c in connections
    )


def _resample(message: FloatMessage, timestamp: np.ndarray) -> FloatMessage:
    if message.is_empty:
        return message

    time, indices = _extrapolate(message.timestamp, timestamp)

    if isinstance(message, OrientationMessage):
        return message._from_rotations(timestamp, scipy.spatial.transform.Slerp(time, message._to_rotations()[indices])(timestamp))

    return replace(message, _csv=np.column_stack((timestamp, scipy.interpolate.interp1d(time, message._csv[indices, 1:], axis=0)(timestamp))))


def _extrapolate(time: np.ndarray, new_time: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    indices = np.arange(len(time))

    if new_time[0] < time[0]:
        time = np.concatenate(([new_time[0]], time))
        indices = np.concatenate(([0], indices))

    if new_time[-1] > time[-1]:
        time = np.concatenate((time, [new_time[-1]]))
        indices = np.concatenate((indices, [indices[-1]]))

    return time, indices
