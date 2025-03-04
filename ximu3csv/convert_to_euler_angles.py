from dataclasses import replace
from typing import List

import numpy as np
import scipy

from .data_messages import EulerAngles
from .device import Device


def __convert_to_euler_angles(device: Device) -> EulerAngles:
    if len(device.quaternion.timestamp) > 0:
        timestamp = device.quaternion.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(device.quaternion.quaternion.wxyz[:, [1, 2, 3, 0]])

    elif len(device.rotation_matrix.timestamp) > 0:
        timestamp = device.rotation_matrix.timestamp
        rotations = scipy.spatial.transform.Rotation.from_matrix(device.rotation_matrix.rotation_matrix.reshape(-1, 3, 3))

    elif len(device.linear_acceleration.timestamp) > 0:
        timestamp = device.linear_acceleration.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(device.linear_acceleration.quaternion.wxyz[:, [1, 2, 3, 0]])

    elif len(device.earth_acceleration.timestamp) > 0:
        timestamp = device.earth_acceleration.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(device.earth_acceleration.quaternion.wxyz[:, [1, 2, 3, 0]])

    else:
        return device.euler_angles

    return EulerAngles(
        _csv=np.column_stack(
            (
                timestamp,
                rotations.as_euler("ZYX", degrees=True)[:, [2, 1, 0]],
            )
        ),
        _string=np.empty([0, 1]),
    )


def convert_to_euler_angles(devices: List[Device]) -> List[Device]:
    return [replace(d, euler_angles=__convert_to_euler_angles(d)) for d in devices]
