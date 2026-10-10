import warnings
from collections.abc import Sequence
from dataclasses import replace

from ..connection import Connection
from ..data_messages import EulerAngles


def create_euler_angles(connections: Sequence[Connection]) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.euler_angles.is_empty:
            warnings.warn(f"Euler angles already exist: {connection}")

    return tuple(replace(c, euler_angles=_create_euler_angles(c)) if c.euler_angles.is_empty else c for c in connections)


def _create_euler_angles(connection: Connection) -> EulerAngles:
    if not connection.quaternion.is_empty:
        return EulerAngles._from_rotations(connection.quaternion.timestamp, connection.quaternion._to_rotations())
    elif not connection.rotation_matrix.is_empty:
        return EulerAngles._from_rotations(connection.rotation_matrix.timestamp, connection.rotation_matrix._to_rotations())
    else:
        return connection.euler_angles
