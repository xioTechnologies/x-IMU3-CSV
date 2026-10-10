from dataclasses import replace

import numpy as np
import scipy

from .connection import Connection
from .data_messages import EulerAngles


def convert_to_euler_angles(connections: list[Connection]) -> list[Connection]:
    return [replace(c, euler_angles=_convert_to_euler_angles(c)) for c in connections]


def _convert_to_euler_angles(connection: Connection) -> EulerAngles:
    if len(connection.quaternion.timestamp) > 0:
        timestamp = connection.quaternion.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(connection.quaternion.wxyz[:, [1, 2, 3, 0]])

    elif len(connection.rotation_matrix.timestamp) > 0:
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
