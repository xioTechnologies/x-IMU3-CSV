from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Union

from .data_messages import (
    AhrsStatus,
    Battery,
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
    interface: Union[None, str]
    device_name: Union[None, str]
    serial_number: Union[None, str]

    # "time" from Command.json
    time: Union[None, datetime]

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
