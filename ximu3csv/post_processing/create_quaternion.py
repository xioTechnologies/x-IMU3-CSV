import warnings
from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection
from ..data_messages import Quaternion


def create_quaternion(connections: Sequence[Connection]) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.quaternion.is_empty:
            warnings.warn(f"Quaternion already exists: {connection}")

    return tuple(replace(c, quaternion=_create_quaternion(c)) if c.quaternion.is_empty else c for c in connections)


def _create_quaternion(connection: Connection) -> Quaternion:
    if not connection.rotation_matrix.is_empty:
        timestamp = connection.rotation_matrix.timestamp
        rotations = scipy.spatial.transform.Rotation.from_matrix(connection.rotation_matrix.xx_to_zz.reshape(-1, 3, 3))
    elif not connection.euler_angles.is_empty:
        timestamp = connection.euler_angles.timestamp
        rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", connection.euler_angles.roll_pitch_yaw[:, [2, 1, 0]], degrees=True)
    else:
        return connection.quaternion

    return Quaternion(
        _csv=np.column_stack(
            (
                timestamp,
                rotations.as_quat()[:, [3, 0, 1, 2]],
            )
        ),
    )
