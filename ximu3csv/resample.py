from dataclasses import replace
from typing import List, Tuple

import numpy as np
import scipy

from .data_messages import (
    DataMessage,
    EarthAcceleration,
    EulerAngles,
    LinearAcceleration,
    Quaternion,
    RotationMatrix,
)
from .device import Device, update_first_and_last_timestamps


def __extrapolate(time: np.ndarray, values: np.ndarray, new_time: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    if new_time[0] < time[0]:
        time = np.concatenate(([new_time[0]], time))
        values = np.concatenate(([values[0, :]], values))

    if new_time[-1] > time[-1]:
        time = np.concatenate((time, [new_time[-1]]))
        values = np.concatenate((values, [values[-1, :]]))

    return time, values


def __interpolate(time: np.ndarray, values: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, values = __extrapolate(time, values, new_time)

    return scipy.interpolate.interp1d(time, values, axis=0)(new_time)


def __slerp_quaternion(time: np.ndarray, quaternion: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, quaternion = __extrapolate(time, quaternion, new_time)

    rotations = scipy.spatial.transform.Rotation.from_quat(quaternion[:, [1, 2, 3, 0]])

    return scipy.spatial.transform.Slerp(time, rotations)(new_time).as_quat()[:, [3, 0, 1, 2]]


def __slerp_euler_angles(time: np.ndarray, euler_angles: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, euler_angles = __extrapolate(time, euler_angles, new_time)

    rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", euler_angles[:, [2, 1, 0]], degrees=True)

    return scipy.spatial.transform.Slerp(time, rotations)(new_time).as_euler("ZYX", degrees=True)[:, [2, 1, 0]]


def __slerp_rotation_matrix(time: np.ndarray, rotation_matrix: np.ndarray, new_time: np.ndarray) -> np.ndarray:
    time, rotation_matrix = __extrapolate(time, rotation_matrix, new_time)

    rotations = scipy.spatial.transform.Rotation.from_matrix(rotation_matrix.reshape(-1, 3, 3))

    return scipy.spatial.transform.Slerp(time, rotations)(new_time).as_matrix().reshape(-1, 9)


def __resample(message: DataMessage, timestamp: np.ndarray) -> DataMessage:
    if len(message.timestamp) == 0:
        return message

    if isinstance(message, (Quaternion, LinearAcceleration, EarthAcceleration)):
        csv = np.column_stack(
            (
                timestamp,
                __slerp_quaternion(message.timestamp / 1e6, message._csv[:, 1:5], timestamp / 1e6),
                __interpolate(message.timestamp / 1e6, message._csv[:, 5:], timestamp / 1e6),
            )
        )
    elif isinstance(message, EulerAngles):
        csv = np.column_stack(
            (
                timestamp,
                __slerp_euler_angles(message.timestamp / 1e6, message._csv[:, 1:], timestamp / 1e6),
            )
        )
    elif isinstance(message, RotationMatrix):
        csv = np.column_stack(
            (
                timestamp,
                __slerp_rotation_matrix(message.timestamp / 1e6, message._csv[:, 1:], timestamp / 1e6),
            )
        )
    else:
        csv = np.column_stack(
            (
                timestamp,
                __interpolate(message.timestamp / 1e6, message._csv[:, 1:], timestamp / 1e6),
            )
        )

    return replace(message, _csv=csv)


def resample(devices: List[Device], sample_rate: float) -> List[Device]:
    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]
    last_timestamps = [d.last_timestamp for d in devices if d.last_timestamp is not None]

    if not first_timestamps or not last_timestamps:
        return devices

    first_timestamp = max(first_timestamps)
    last_timestamp = min(last_timestamps)

    if first_timestamps == last_timestamps:
        return devices

    timestamp = np.arange(first_timestamp, last_timestamp, 1e6 / sample_rate)

    devices = [
        replace(
            d,
            inertial=__resample(d.inertial, timestamp),
            magnetometer=__resample(d.magnetometer, timestamp),
            quaternion=__resample(d.quaternion, timestamp),
            rotation_matrix=__resample(d.rotation_matrix, timestamp),
            euler_angles=__resample(d.euler_angles, timestamp),
            linear_acceleration=__resample(d.linear_acceleration, timestamp),
            earth_acceleration=__resample(d.earth_acceleration, timestamp),
            high_g_accelerometer=__resample(d.high_g_accelerometer, timestamp),
            temperature=__resample(d.temperature, timestamp),
            battery=__resample(d.battery, timestamp),
            rssi=__resample(d.rssi, timestamp),
            serial_accessory=__resample(d.serial_accessory, timestamp),
        )
        for d in devices
    ]

    return [update_first_and_last_timestamps(d) for d in devices]
