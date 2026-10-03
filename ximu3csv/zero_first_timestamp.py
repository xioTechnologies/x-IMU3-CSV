from dataclasses import replace

import numpy as np

from .data_messages import DataMessage
from .device import Device, update_first_and_last_timestamps


def _zero_first_timestamp(message: DataMessage, first_timestamp: int) -> DataMessage:
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


def zero_first_timestamp(devices: list[Device], offset: int = 0) -> list[Device]:
    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]

    if not first_timestamps:
        return devices

    first_timestamp = min(first_timestamps) - offset

    devices = [
        replace(
            d,
            inertial=_zero_first_timestamp(d.inertial, first_timestamp),
            magnetometer=_zero_first_timestamp(d.magnetometer, first_timestamp),
            high_g_accelerometer=_zero_first_timestamp(d.high_g_accelerometer, first_timestamp),
            quaternion=_zero_first_timestamp(d.quaternion, first_timestamp),
            rotation_matrix=_zero_first_timestamp(d.rotation_matrix, first_timestamp),
            euler_angles=_zero_first_timestamp(d.euler_angles, first_timestamp),
            linear_acceleration=_zero_first_timestamp(d.linear_acceleration, first_timestamp),
            earth_acceleration=_zero_first_timestamp(d.earth_acceleration, first_timestamp),
            ahrs_status=_zero_first_timestamp(d.ahrs_status, first_timestamp),
            serial_accessory=_zero_first_timestamp(d.serial_accessory, first_timestamp),
            sync=_zero_first_timestamp(d.sync, first_timestamp),
            ltc=_zero_first_timestamp(d.ltc, first_timestamp),
            temperature=_zero_first_timestamp(d.temperature, first_timestamp),
            battery=_zero_first_timestamp(d.battery, first_timestamp),
            rssi=_zero_first_timestamp(d.rssi, first_timestamp),
            button=_zero_first_timestamp(d.button, first_timestamp),
            notification=_zero_first_timestamp(d.notification, first_timestamp),
            error=_zero_first_timestamp(d.error, first_timestamp),
        )
        for d in devices
    ]

    return [update_first_and_last_timestamps(d) for d in devices]
