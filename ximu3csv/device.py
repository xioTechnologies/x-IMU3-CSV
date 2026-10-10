from dataclasses import dataclass, fields
from datetime import datetime
from functools import cached_property
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

    @cached_property
    def first_timestamp(self) -> float | None:
        timestamps = [m.timestamp[0] for m in self._data_messages() if len(m.timestamp) > 0]

        return min(timestamps) if timestamps else None

    @cached_property
    def last_timestamp(self) -> float | None:
        timestamps = [m.timestamp[-1] for m in self._data_messages() if len(m.timestamp) > 0]

        return max(timestamps) if timestamps else None

    def _data_messages(self) -> list[DataMessage]:
        return [getattr(self, f.name) for f in fields(self) if isinstance(getattr(self, f.name), DataMessage)]
