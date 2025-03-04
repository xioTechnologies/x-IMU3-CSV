from dataclasses import dataclass, fields, replace
from datetime import datetime
from typing import Any, Dict, List, Optional

from .data_messages import (
    AhrsStatus,
    Battery,
    DataMessage,
    EarthAcceleration,
    Error,
    EulerAngles,
    HighGAccelerometer,
    Inertial,
    LinearAcceleration,
    Magnetometer,
    Notification,
    Quaternion,
    RotationMatrix,
    Rssi,
    SerialAccessory,
    Temperature,
)


@dataclass(frozen=True)
class Device:
    # Command.json
    command: List[Dict[str, Any]]

    # "ping" from Command.json
    interface: Optional[str]
    device_name: Optional[str]
    serial_number: Optional[str]

    # "time" from Command.json
    time: Optional[datetime]

    # *.csv files
    inertial: Inertial
    magnetometer: Magnetometer
    quaternion: Quaternion
    rotation_matrix: RotationMatrix
    euler_angles: EulerAngles
    linear_acceleration: LinearAcceleration
    earth_acceleration: EarthAcceleration
    ahrs_status: AhrsStatus
    high_g_accelerometer: HighGAccelerometer
    temperature: Temperature
    battery: Battery
    rssi: Rssi
    serial_accessory: SerialAccessory
    notification: Notification
    error: Error

    # first and last timestamps from *.csv files
    first_timestamp: Optional[int]
    last_timestamp: Optional[int]


def update_first_and_last_timestamps(device: Device) -> Device:
    device = replace(device, first_timestamp=None)
    device = replace(device, last_timestamp=None)

    for field in fields(device):
        attribute = getattr(device, field.name)

        if not isinstance(attribute, DataMessage):
            continue

        if len(attribute.timestamp) == 0:
            continue

        if device.first_timestamp is None or attribute.timestamp[0] < device.first_timestamp:
            device = replace(device, first_timestamp=attribute.timestamp[0])

        if device.last_timestamp is None or attribute.timestamp[-1] > device.last_timestamp:
            device = replace(device, last_timestamp=attribute.timestamp[-1])

    return device
