import warnings
from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection, max_last_timestamp
from ..data_messages import OrientationMessage


def set_heading(connections: Sequence[Connection], heading: float, timestamp: float | None) -> tuple[Connection, ...]:
    last_timestamp = max_last_timestamp(connections)

    if (timestamp is not None) and (last_timestamp is not None) and (timestamp > last_timestamp):
        raise ValueError(f"Timestamp is after last timestamp: {timestamp} > {last_timestamp}")

    if any(not c.earth_acceleration.is_empty for c in connections):
        warnings.warn("Heading not set for earth acceleration")

    return tuple(
        replace(
            c,
            quaternion=_set_heading_message(c.quaternion, heading, timestamp),
            rotation_matrix=_set_heading_message(c.rotation_matrix, heading, timestamp),
            euler_angles=_set_heading_message(c.euler_angles, heading, timestamp),
        )
        for c in connections
    )


def _set_heading_message(message: OrientationMessage, heading: float, timestamp: float | None) -> OrientationMessage:
    if message.is_empty:
        return message

    if (timestamp is not None) and (timestamp > message.timestamp[-1]):
        return message

    index = 0 if timestamp is None else np.argmax(message.timestamp >= timestamp)

    return message._from_rotations(message.timestamp, _set_heading_rotations(message._to_rotations(), heading, index))


def _set_heading_rotations(rotations: scipy.spatial.transform.Rotation, heading: float, index: int) -> scipy.spatial.transform.Rotation:
    angle = heading - rotations[index].as_euler("ZYX", degrees=True)[0]

    rotations[index:] = scipy.spatial.transform.Rotation.from_euler("Z", angle, degrees=True) * rotations[index:]

    return rotations


def zero_heading(connections: Sequence[Connection], timestamp: float | None) -> tuple[Connection, ...]:
    return set_heading(connections, 0, timestamp)
