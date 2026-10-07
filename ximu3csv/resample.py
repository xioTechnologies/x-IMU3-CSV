from dataclasses import replace

import numpy as np
import scipy

from .data_messages import (
    EulerAngles,
    FloatMessage,
    Quaternion,
    RotationMatrix,
)
from .device import Device


def _extrapolate(time: np.ndarray, values: np.ndarray, new_time: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if new_time[0] < time[0]:
        time = np.concatenate(([new_time[0]], time))
        values = np.concatenate(([values[0, :]], values))

    if new_time[-1] > time[-1]:
        time = np.concatenate((time, [new_time[-1]]))
        values = np.concatenate((values, [values[-1, :]]))

    return time, values


def _interpolate(time: np.ndarray, values: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, values = _extrapolate(time, values, new_time)

    return scipy.interpolate.interp1d(time, values, axis=0)(new_time)


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


def resample(devices: list[Device], sample_rate: float) -> list[Device]:
    if sample_rate <= 0:
        raise ValueError(f"Invalid sample rate: {sample_rate} Hz")

    if all(d.first_timestamp is None for d in devices):
        raise ValueError("No timestamps")

    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]
    last_timestamps = [d.last_timestamp for d in devices if d.last_timestamp is not None]

    first_timestamp = max(first_timestamps)
    last_timestamp = min(last_timestamps)

    if first_timestamp >= last_timestamp:
        raise ValueError("No overlapping timestamps")

    timestamp = np.arange(first_timestamp, last_timestamp, 1e6 / sample_rate)

    return [
        replace(
            d,
            inertial=_resample(d.inertial, timestamp),
            magnetometer=_resample(d.magnetometer, timestamp),
            high_g_accelerometer=_resample(d.high_g_accelerometer, timestamp),
            quaternion=_resample(d.quaternion, timestamp),
            rotation_matrix=_resample(d.rotation_matrix, timestamp),
            euler_angles=_resample(d.euler_angles, timestamp),
            linear_acceleration=_resample(d.linear_acceleration, timestamp),
            earth_acceleration=_resample(d.earth_acceleration, timestamp),
            sync=_resample(d.sync, timestamp),  # TODO: Do not interpolate edges
            temperature=_resample(d.temperature, timestamp),
            battery=_resample(d.battery, timestamp),
            rssi=_resample(d.rssi, timestamp),
            button=_resample(d.button, timestamp),  # TODO: Do not interpolate edges
        )
        for d in devices
    ]
