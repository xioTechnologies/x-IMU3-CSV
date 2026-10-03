from dataclasses import dataclass, fields, replace
from datetime import datetime
from typing import Any

from .data_messages import (
    AhrsStatus,
    Battery,
    Button,
    DataMessage,
    EarthAcceleration,
    Error,
    EulerAngles,
    HighGAccelerometer,
    Inertial,
    LinearAcceleration,
    Ltc,
    Magnetometer,
    Notification,
    Quaternion,
    RotationMatrix,
    Rssi,
    SerialAccessory,
    Sync,
    Temperature,
)


@dataclass(frozen=True)
class Device:
    # Command.json
    command: list[dict[str, Any]]

    # "ping" from Command.json
    interface: str | None
    device_name: str | None
    serial_number: str | None

    # "time" from Command.json
    time: datetime | None

    # *.csv files
    inertial: Inertial
    magnetometer: Magnetometer
    high_g_accelerometer: HighGAccelerometer
    quaternion: Quaternion
    rotation_matrix: RotationMatrix
    euler_angles: EulerAngles
    linear_acceleration: LinearAcceleration
    earth_acceleration: EarthAcceleration
    ahrs_status: AhrsStatus
    serial_accessory: SerialAccessory
    sync: Sync
    ltc: Ltc
    temperature: Temperature
    battery: Battery
    rssi: Rssi
    button: Button
    notification: Notification
    error: Error

    # first and last timestamps from *.csv files
    first_timestamp: int | None
    last_timestamp: int | None


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
            device = replace(device, first_timestamp=int(attribute.timestamp[0]))

        if device.last_timestamp is None or attribute.timestamp[-1] > device.last_timestamp:
            device = replace(device, last_timestamp=int(attribute.timestamp[-1]))

    return device
