import warnings
from collections.abc import Sequence
from dataclasses import replace

import numpy as np
import scipy

from ..connection import Connection
from ..data_messages import EarthAcceleration


def create_earth_acceleration(connections: Sequence[Connection], z_up: bool) -> tuple[Connection, ...]:
    for connection in connections:
        if not connection.earth_acceleration.is_empty:
            warnings.warn(f"Earth acceleration already exists: {connection}")

    return tuple(replace(c, earth_acceleration=_create_earth_acceleration(c, z_up)) if c.earth_acceleration.is_empty else c for c in connections)


def _create_earth_acceleration(connection: Connection, z_up: bool) -> EarthAcceleration:
    if connection.inertial.is_empty:
        raise ValueError(f"No inertial: {connection}")

    if not connection.quaternion.is_empty:
        timestamp = connection.quaternion.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(connection.quaternion.wxyz[:, [1, 2, 3, 0]])
    elif not connection.rotation_matrix.is_empty:
        timestamp = connection.rotation_matrix.timestamp
        rotations = scipy.spatial.transform.Rotation.from_matrix(connection.rotation_matrix.xx_to_zz.reshape(-1, 3, 3))
    elif not connection.euler_angles.is_empty:
        timestamp = connection.euler_angles.timestamp
        rotations = scipy.spatial.transform.Rotation.from_euler("ZYX", connection.euler_angles.roll_pitch_yaw[:, [2, 1, 0]], degrees=True)
    else:
        raise ValueError(f"No orientation: {connection}")

    mask = (connection.inertial.timestamp >= timestamp[0]) & (connection.inertial.timestamp <= timestamp[-1])

    rotations = scipy.spatial.transform.Slerp(timestamp, rotations)(connection.inertial.timestamp[mask])

    gravity = [0, 0, 1] if z_up else [0, 0, -1]

    return EarthAcceleration(
        _csv=np.column_stack(
            (
                connection.inertial.timestamp[mask],
                rotations.apply(connection.inertial.accelerometer_xyz[mask]) - gravity,
            )
        ),
    )
