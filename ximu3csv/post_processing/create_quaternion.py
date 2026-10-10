import warnings
from collections.abc import Sequence
from dataclasses import replace

from ..connection import Connection
from ..data_messages import Quaternion


def create_quaternion(connections: Sequence[Connection]) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.quaternion.is_empty:
            warnings.warn(f"Quaternion already exists: {connection}")

    return tuple(replace(c, quaternion=_create_quaternion(c)) if c.quaternion.is_empty else c for c in connections)


def _create_quaternion(connection: Connection) -> Quaternion:
    if not connection.rotation_matrix.is_empty:
        return Quaternion._from_rotations(connection.rotation_matrix.timestamp, connection.rotation_matrix._to_rotations())
    elif not connection.euler_angles.is_empty:
        return Quaternion._from_rotations(connection.euler_angles.timestamp, connection.euler_angles._to_rotations())
    else:
        return connection.quaternion
