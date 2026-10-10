import warnings
from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection
from ..data_messages import RotationMatrix


def calculate_rotation_matrix(connections: Sequence[Connection]) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.rotation_matrix.is_empty:
            warnings.warn(f"Rotation matrix already exists for {connection}")  # TODO: implement printable identifier for Connection

    return tuple(replace(c, rotation_matrix=_calculate_rotation_matrix(c)) if c.rotation_matrix.is_empty else c for c in connections)


def _calculate_rotation_matrix(connection: Connection) -> RotationMatrix:
    if not connection.quaternion.is_empty:
        timestamp = connection.quaternion.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(connection.quaternion.wxyz[:, [1, 2, 3, 0]])
    elif not connection.euler_angles.is_empty:
        timestamp = connection.euler_angles.timestamp
        rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", connection.euler_angles.roll_pitch_yaw[:, [2, 1, 0]], degrees=True)
    else:
        return connection.rotation_matrix

    return RotationMatrix(
        _csv=np.column_stack(
            (
                timestamp,
                rotations.as_matrix().reshape(-1, 9),
            )
        ),
    )
