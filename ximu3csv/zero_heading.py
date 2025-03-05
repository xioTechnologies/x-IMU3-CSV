from dataclasses import replace
from typing import List

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
from .device import Device


def __zero_heading_rotations(rotations: List[scipy.spatial.transform.Rotation], index: int, offset: float) -> List[scipy.spatial.transform.Rotation]:
    angle = offset - rotations[index].as_euler("ZYX", degrees=True)[0]

    rotations[index:] = scipy.spatial.transform.Rotation.from_euler("Z", angle, degrees=True) * rotations[index:]

    return rotations


def __zero_heading_message(message: DataMessage, timestamp: int, offset: float) -> DataMessage:
    if len(message.timestamp) == 0:
        return message

    if timestamp > message.timestamp[-1]:
        return message

    index = np.argmax(message.timestamp >= timestamp)

    if isinstance(message, (Quaternion, LinearAcceleration, EarthAcceleration)):
        rotations = scipy.spatial.transform.Rotation.from_quat(message.quaternion.wxyz[:, [1, 2, 3, 0]])

        csv = np.column_stack(
            (
                message.timestamp,
                __zero_heading_rotations(rotations, index, offset).as_quat()[:, [3, 0, 1, 2]],
                message._csv[:, 5:],
            )
        )
    elif isinstance(message, EulerAngles):
        rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", message.euler_angles[:, [2, 1, 0]], degrees=True)

        csv = np.column_stack(
            (
                message.timestamp,
                __zero_heading_rotations(rotations, index, offset).as_euler("ZYX", degrees=True)[:, [2, 1, 0]],
            )
        )
    elif isinstance(message, RotationMatrix):
        rotations = scipy.spatial.transform.Rotation.from_matrix(message.rotation_matrix.reshape(-1, 3, 3))

        csv = np.column_stack(
            (
                message.timestamp,
                __zero_heading_rotations(rotations, index, offset).as_matrix().reshape(-1, 9),
            )
        )

    return replace(message, _csv=csv)


def zero_heading(devices: List[Device], timestamp: int = 0, offset: float = 0) -> List[Device]:
    return [
        replace(
            d,
            quaternion=__zero_heading_message(d.quaternion, timestamp, offset),
            rotation_matrix=__zero_heading_message(d.rotation_matrix, timestamp, offset),
            euler_angles=__zero_heading_message(d.euler_angles, timestamp, offset),
            linear_acceleration=__zero_heading_message(d.linear_acceleration, timestamp, offset),
            earth_acceleration=__zero_heading_message(d.earth_acceleration, timestamp, offset),
        )
        for d in devices
    ]
