import warnings
from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection
from ..data_messages import EulerAngles


def create_euler_angles(connections: Sequence[Connection]) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.euler_angles.is_empty:
            warnings.warn(f"Euler angles already exist: {connection}")

    return tuple(replace(c, euler_angles=_create_euler_angles(c)) if c.euler_angles.is_empty else c for c in connections)


def _create_euler_angles(connection: Connection) -> EulerAngles:
    if not connection.quaternion.is_empty:
        timestamp = connection.quaternion.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(connection.quaternion.wxyz[:, [1, 2, 3, 0]])
    elif not connection.rotation_matrix.is_empty:
        timestamp = connection.rotation_matrix.timestamp
        rotations = scipy.spatial.transform.Rotation.from_matrix(connection.rotation_matrix.xx_to_zz.reshape(-1, 3, 3))
    else:
        return connection.euler_angles

    return EulerAngles(
        _csv=np.column_stack(
            (
                timestamp,
                rotations.as_euler("ZYX", degrees=True)[:, [2, 1, 0]],
            )
        ),
    )
