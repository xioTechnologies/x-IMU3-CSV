import warnings
from dataclasses import replace

import numpy as np
import scipy

from .data_messages import (
    EulerAngles,
    FloatMessage,
    Quaternion,
    RotationMatrix,
)
from .logged_data import LoggedData


def zero_heading(data: LoggedData, timestamp: float | None = None) -> LoggedData:
    return set_heading(data, 0, timestamp)


def set_heading(data: LoggedData, heading: float, timestamp: float | None = None) -> LoggedData:
    if (timestamp is not None) and (data.last_timestamp is not None) and (timestamp > data.last_timestamp):
        raise ValueError(f"Timestamp is after last timestamp: {timestamp} > {data.last_timestamp}")

    if any(len(c.earth_acceleration.timestamp) > 0 for c in data):
        warnings.warn("Heading not set for earth acceleration")

    connections = tuple(
        replace(
            c,
            quaternion=_set_heading_message(c.quaternion, heading, timestamp),
            rotation_matrix=_set_heading_message(c.rotation_matrix, heading, timestamp),
            euler_angles=_set_heading_message(c.euler_angles, heading, timestamp),
        )
        for c in data
    )

    return replace(data, _connections=connections)


def _set_heading_message(message: FloatMessage, heading: float, timestamp: float | None) -> FloatMessage:
    if len(message.timestamp) == 0:
        return message

    if (timestamp is not None) and (timestamp > message.timestamp[-1]):
        return message

    index = 0 if timestamp is None else np.argmax(message.timestamp >= timestamp)

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

    return replace(message, _csv=csv)


def _set_heading_rotations(rotations: scipy.spatial.transform.Rotation, heading: float, index: int) -> scipy.spatial.transform.Rotation:
    angle = heading - rotations[index].as_euler("ZYX", degrees=True)[0]

    rotations[index:] = scipy.spatial.transform.Rotation.from_euler("Z", angle, degrees=True) * rotations[index:]

    return rotations
