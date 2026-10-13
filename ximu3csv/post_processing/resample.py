import warnings
from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection, max_last_timestamp, min_first_timestamp
from ..data_messages import Battery, FloatMessage, OrientationMessage


def resample(connections: Sequence[Connection], sample_rate: float) -> tuple[Connection, ...]:
    if sample_rate <= 0:
        raise ValueError(f"Invalid sample rate: {sample_rate}")

    first_timestamp = min_first_timestamp(connections)
    last_timestamp = max_last_timestamp(connections)

    if (first_timestamp is None) or (last_timestamp is None):
        raise ValueError("No timestamps")

    if any(not c.ahrs_status.is_empty for c in connections):
        warnings.warn("AHRS status not resampled")

    if any(not c.serial_accessory.is_empty for c in connections):
        warnings.warn("Serial accessory not resampled")

    if any(not c.sync.is_empty for c in connections):
        warnings.warn("Sync not resampled")

    if any(not c.ltc.is_empty for c in connections):
        warnings.warn("LTC not resampled")

    if any(not c.button.is_empty for c in connections):
        warnings.warn("Button not resampled")

    if any(not c.notification.is_empty for c in connections):
        warnings.warn("Notification not resampled")

    if any(not c.error.is_empty for c in connections):
        warnings.warn("Error not resampled")

    if any(not c.battery.is_empty for c in connections):
        warnings.warn("Battery charging status not resampled")

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
            temperature=_resample(c.temperature, timestamp),
            battery=_resample(c.battery, timestamp),
            rssi=_resample(c.rssi, timestamp),
        )
        for c in connections
    )


def _resample(message: FloatMessage, timestamp: np.ndarray) -> FloatMessage:
    if message.is_empty:
        return message

    time, indices = _extrapolate(message.timestamp, timestamp)

    if isinstance(message, OrientationMessage):
        return message._from_rotation(timestamp, scipy.spatial.transform.Slerp(time, message._to_rotation()[indices])(timestamp))
    elif isinstance(message, Battery):
        return replace(message, _csv=np.column_stack((timestamp, scipy.interpolate.interp1d(time, message._csv[indices, 1:3], axis=0)(timestamp), np.full(len(timestamp), np.nan))))  # set charging status to NaN
    else:
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
