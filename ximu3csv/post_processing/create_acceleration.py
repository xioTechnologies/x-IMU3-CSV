import warnings
from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection
from ..data_messages import EarthAcceleration, LinearAcceleration


def create_linear_acceleration(connections: Sequence[Connection], z_up: bool) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.linear_acceleration.is_empty:
            warnings.warn(f"Linear acceleration already exists: {connection}")

    return tuple(replace(c, linear_acceleration=_create_linear_acceleration(c, z_up)) if c.linear_acceleration.is_empty else c for c in connections)


def create_earth_acceleration(connections: Sequence[Connection], z_up: bool) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.earth_acceleration.is_empty:
            warnings.warn(f"Earth acceleration already exists: {connection}")

    return tuple(replace(c, earth_acceleration=_create_earth_acceleration(c, z_up)) if c.earth_acceleration.is_empty else c for c in connections)


def _create_linear_acceleration(connection: Connection, z_up: bool) -> LinearAcceleration:
    timestamp, accelerometer, rotations = _get_accelerometer_and_rotations(connection)

    gravity = [0, 0, 1] if z_up else [0, 0, -1]

    return LinearAcceleration(np.column_stack((timestamp, accelerometer - rotations.inv().apply(gravity))))


def _create_earth_acceleration(connection: Connection, z_up: bool) -> EarthAcceleration:
    timestamp, accelerometer, rotations = _get_accelerometer_and_rotations(connection)

    gravity = [0, 0, 1] if z_up else [0, 0, -1]

    return EarthAcceleration(np.column_stack((timestamp, rotations.apply(accelerometer) - gravity)))


def _get_accelerometer_and_rotations(connection: Connection) -> tuple[np.ndarray, np.ndarray, scipy.spatial.transform.Rotation]:
    if connection.inertial.is_empty:
        raise ValueError(f"No inertial: {connection}")

    if not connection.quaternion.is_empty:
        orientation = connection.quaternion
    elif not connection.rotation_matrix.is_empty:
        orientation = connection.rotation_matrix
    elif not connection.euler_angles.is_empty:
        orientation = connection.euler_angles
    else:
        raise ValueError(f"No orientation: {connection}")

    mask = (connection.inertial.timestamp >= orientation.timestamp[0]) & (connection.inertial.timestamp <= orientation.timestamp[-1])

    timestamp = connection.inertial.timestamp[mask]

    rotations = scipy.spatial.transform.Slerp(orientation.timestamp, orientation._to_rotations())(timestamp)

    return timestamp, connection.inertial.accelerometer_xyz[mask], rotations
