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


def _zero_heading_rotations(rotations: scipy.spatial.transform.Rotation, index: int, offset: float) -> scipy.spatial.transform.Rotation:
    angle = offset - rotations[index].as_euler("ZYX", degrees=True)[0]

    rotations[index:] = scipy.spatial.transform.Rotation.from_euler("Z", angle, degrees=True) * rotations[index:]

    return rotations


def _zero_heading_message(message: FloatMessage, timestamp: int, offset: float) -> FloatMessage:
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
                _zero_heading_rotations(rotations, index, offset).as_quat()[:, [3, 0, 1, 2]],
            )
        )
    elif isinstance(message, EulerAngles):
        rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", message.roll_pitch_yaw[:, [2, 1, 0]], degrees=True)

        csv = np.column_stack(
            (
                message.timestamp,
                _zero_heading_rotations(rotations, index, offset).as_euler("ZYX", degrees=True)[:, [2, 1, 0]],
            )
        )
    elif isinstance(message, RotationMatrix):
        rotations = scipy.spatial.transform.Rotation.from_matrix(message.xx_to_zz.reshape(-1, 3, 3))

        csv = np.column_stack(
            (
                message.timestamp,
                _zero_heading_rotations(rotations, index, offset).as_matrix().reshape(-1, 9),
            )
        )

    return replace(message, _csv=csv)


def zero_heading(devices: list[Device], timestamp: int = 0, offset: float = 0) -> list[Device]:
    return [
        replace(
            d,
            quaternion=_zero_heading_message(d.quaternion, timestamp, offset),
            rotation_matrix=_zero_heading_message(d.rotation_matrix, timestamp, offset),
            euler_angles=_zero_heading_message(d.euler_angles, timestamp, offset),
            # TODO: Rotate earth_acceleration
        )
        for d in devices
    ]
