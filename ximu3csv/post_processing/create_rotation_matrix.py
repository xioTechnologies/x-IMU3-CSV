import warnings
from collections.abc import Sequence
from dataclasses import replace

from ..connection import Connection
from ..data_messages import RotationMatrix


def create_rotation_matrix(connections: Sequence[Connection]) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.rotation_matrix.is_empty:
            warnings.warn(f"Rotation matrix already exists: {connection}")

    return tuple(replace(c, rotation_matrix=_create_rotation_matrix(c)) if c.rotation_matrix.is_empty else c for c in connections)


def _create_rotation_matrix(connection: Connection) -> RotationMatrix:
    if not connection.quaternion.is_empty:
        return RotationMatrix._from_rotations(connection.quaternion.timestamp, connection.quaternion._to_rotations())
    elif not connection.euler_angles.is_empty:
        return RotationMatrix._from_rotations(connection.euler_angles.timestamp, connection.euler_angles._to_rotations())
    else:
        return connection.rotation_matrix
