from dataclasses import replace

import numpy as np
import scipy

from .data_messages import EulerAngles
from .device import Device


def convert_to_euler_angles(devices: list[Device]) -> list[Device]:
    return [replace(d, euler_angles=_convert_to_euler_angles(d)) for d in devices]


def _convert_to_euler_angles(device: Device) -> EulerAngles:
    if len(device.quaternion.timestamp) > 0:
        timestamp = device.quaternion.timestamp
        rotations = scipy.spatial.transform.Rotation.from_quat(device.quaternion.wxyz[:, [1, 2, 3, 0]])

    elif len(device.rotation_matrix.timestamp) > 0:
        timestamp = device.rotation_matrix.timestamp
        rotations = scipy.spatial.transform.Rotation.from_matrix(device.rotation_matrix.xx_to_zz.reshape(-1, 3, 3))

    else:
        return device.euler_angles

    return EulerAngles(
        _csv=np.column_stack(
            (
                timestamp,
                rotations.as_euler("ZYX", degrees=True)[:, [2, 1, 0]],
            )
        ),
    )
