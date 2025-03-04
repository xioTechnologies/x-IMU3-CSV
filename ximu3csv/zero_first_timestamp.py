from dataclasses import replace
from typing import List

import numpy as np

from .data_messages import DataMessage
from .device import Device, update_first_and_last_timestamps


def __zero_first_timestamp(message: DataMessage, first_timestamp: int) -> DataMessage:
    if len(message.timestamp) == 0:
        return message

    return replace(
        message,
        _csv=np.column_stack(
            (
                message._csv[:, 0] - first_timestamp,
                message._csv[:, 1:],
            ),
        ),
    )


def zero_first_timestamp(devices: List[Device], offset: int = 0) -> List[Device]:
    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]

    if not first_timestamps:
        return devices

    first_timestamp = min(first_timestamps) - offset

    devices = [
        replace(
            d,
            inertial=__zero_first_timestamp(d.inertial, first_timestamp),
            magnetometer=__zero_first_timestamp(d.magnetometer, first_timestamp),
            quaternion=__zero_first_timestamp(d.quaternion, first_timestamp),
            rotation_matrix=__zero_first_timestamp(d.rotation_matrix, first_timestamp),
            euler_angles=__zero_first_timestamp(d.euler_angles, first_timestamp),
            linear_acceleration=__zero_first_timestamp(d.linear_acceleration, first_timestamp),
            earth_acceleration=__zero_first_timestamp(d.earth_acceleration, first_timestamp),
            ahrs_status=__zero_first_timestamp(d.ahrs_status, first_timestamp),
            high_g_accelerometer=__zero_first_timestamp(d.high_g_accelerometer, first_timestamp),
            temperature=__zero_first_timestamp(d.temperature, first_timestamp),
            battery=__zero_first_timestamp(d.battery, first_timestamp),
            rssi=__zero_first_timestamp(d.rssi, first_timestamp),
            serial_accessory=__zero_first_timestamp(d.serial_accessory, first_timestamp),
            notification=__zero_first_timestamp(d.notification, first_timestamp),
            error=__zero_first_timestamp(d.error, first_timestamp),
        )
        for d in devices
    ]

    return [update_first_and_last_timestamps(d) for d in devices]
