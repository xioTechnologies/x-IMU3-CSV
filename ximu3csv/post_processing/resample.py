from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection
from ..data_messages import (
    EulerAngles,
    FloatMessage,
    Quaternion,
    RotationMatrix,
)


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
    if len(message.timestamp) == 0:
        return message

    if isinstance(message, Quaternion):
        csv = np.column_stack(
            (
                timestamp,
                _slerp_quaternion(message.timestamp / 1e6, message._csv[:, 1:], timestamp / 1e6),
            )
        )
    elif isinstance(message, EulerAngles):
        csv = np.column_stack(
            (
                timestamp,
                _slerp_euler_angles(message.timestamp / 1e6, message._csv[:, 1:], timestamp / 1e6),
            )
        )
    elif isinstance(message, RotationMatrix):
        csv = np.column_stack(
            (
                timestamp,
                _slerp_rotation_matrix(message.timestamp / 1e6, message._csv[:, 1:], timestamp / 1e6),
            )
        )
    else:
        csv = np.column_stack(
            (
                timestamp,
                _interpolate(message.timestamp / 1e6, message._csv[:, 1:], timestamp / 1e6),
            )
        )

    return replace(message, _csv=csv)


def _slerp_quaternion(time: np.ndarray, quaternion: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, quaternion = _extrapolate(time, quaternion, new_time)

    rotations = scipy.spatial.transform.Rotation.from_quat(quaternion[:, [1, 2, 3, 0]])

    return scipy.spatial.transform.Slerp(time, rotations)(new_time).as_quat()[:, [3, 0, 1, 2]]


def _slerp_euler_angles(time: np.ndarray, euler_angles: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, euler_angles = _extrapolate(time, euler_angles, new_time)

    rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", euler_angles[:, [2, 1, 0]], degrees=True)

    return scipy.spatial.transform.Slerp(time, rotations)(new_time).as_euler("ZYX", degrees=True)[:, [2, 1, 0]]


def _slerp_rotation_matrix(time: np.ndarray, rotation_matrix: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, rotation_matrix = _extrapolate(time, rotation_matrix, new_time)

    rotations = scipy.spatial.transform.Rotation.from_matrix(rotation_matrix.reshape(-1, 3, 3))

    return scipy.spatial.transform.Slerp(time, rotations)(new_time).as_matrix().reshape(-1, 9)


def _interpolate(time: np.ndarray, values: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, values = _extrapolate(time, values, new_time)

    return scipy.interpolate.interp1d(time, values, axis=0)(new_time)


def _extrapolate(time: np.ndarray, values: np.ndarray, new_time: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if new_time[0] < time[0]:
        time = np.concatenate(([new_time[0]], time))
        values = np.concatenate(([values[0, :]], values))

    if new_time[-1] > time[-1]:
        time = np.concatenate((time, [new_time[-1]]))
        values = np.concatenate((values, [values[-1, :]]))

    return time, values
