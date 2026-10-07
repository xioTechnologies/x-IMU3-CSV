from dataclasses import replace

import numpy as np
import scipy

from .data_messages import (
    EarthAcceleration,
    EulerAngles,
    FloatMessage,
    Quaternion,
    RotationMatrix,
)
from .device import Device


def zero_heading(devices: list[Device], timestamp: int = 0) -> list[Device]:
    return set_heading(devices, 0, timestamp)


def set_heading(devices: list[Device], heading: float, timestamp: int = 0) -> list[Device]:
    last_timestamp = max((d.last_timestamp for d in devices if d.last_timestamp is not None), default=None)

    if (last_timestamp is not None) and (timestamp > last_timestamp):
        raise ValueError(f"Timestamp is after last timestamp: {timestamp} > {last_timestamp}")

    return [
        replace(
            d,
            quaternion=_set_heading_message(d.quaternion, heading, timestamp),
            rotation_matrix=_set_heading_message(d.rotation_matrix, heading, timestamp),
            euler_angles=_set_heading_message(d.euler_angles, heading, timestamp),
            earth_acceleration=_set_heading_message(d.earth_acceleration, heading, timestamp),
        )
        for d in devices
    ]


def _set_heading_message(message: FloatMessage, heading: float, timestamp: int) -> FloatMessage:
    if len(message.timestamp) == 0:
        return message

    if timestamp > message.timestamp[-1]:
        return message

    index = np.argmax(message.timestamp >= timestamp)

    if isinstance(message, Quaternion):
        rotations = scipy.spatial.transform.Rotation.from_quat(message.wxyz[:, [1, 2, 3, 0]])

        csv = np.column_stack(
            (
                message.timestamp,
                _set_heading_rotations(rotations, heading, index).as_quat()[:, [3, 0, 1, 2]],
            )
        )
    elif isinstance(message, EulerAngles):
        rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", message.roll_pitch_yaw[:, [2, 1, 0]], degrees=True)

        csv = np.column_stack(
            (
                message.timestamp,
                _set_heading_rotations(rotations, heading, index).as_euler("ZYX", degrees=True)[:, [2, 1, 0]],
            )
        )
    elif isinstance(message, RotationMatrix):
        rotations = scipy.spatial.transform.Rotation.from_matrix(message.xx_to_zz.reshape(-1, 3, 3))

        csv = np.column_stack(
            (
                message.timestamp,
                _set_heading_rotations(rotations, heading, index).as_matrix().reshape(-1, 9),
            )
        )
    elif isinstance(message, EarthAcceleration):
        raise NotImplementedError("Set heading of earth acceleration")  # TODO

    return replace(message, _csv=csv)


def _set_heading_rotations(rotations: scipy.spatial.transform.Rotation, heading: float, index: int) -> scipy.spatial.transform.Rotation:
    angle = heading - rotations[index].as_euler("ZYX", degrees=True)[0]

    rotations[index:] = scipy.spatial.transform.Rotation.from_euler("Z", angle, degrees=True) * rotations[index:]

    return rotations
