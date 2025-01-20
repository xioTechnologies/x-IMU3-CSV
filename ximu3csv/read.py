import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union

import numpy as np

from .data_messages import (
    AhrsStatus,
    Battery,
    DataMessageType,
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
from .device import Device


def _read_command(directory: str) -> List[Dict[str, Any]]:
    file_path = os.path.join(directory, "Command.json")

    if not os.path.isfile(file_path):
        return []

    with open(file_path) as file:
        return json.load(file)


def _parse_ping(command: List[Dict[str, Any]]) -> Union[Tuple[None, None, None], Tuple[str, str, str]]:
    for response in command:
        for key, value in response.items():
            if key == "ping":
                try:
                    return value["interface"], value["name"], value["sn"]
                except Exception as _:
                    print(f"Unable to parse ping response {value}")

    return None, None, None


def _parse_time(command: List[Dict[str, Any]]) -> datetime:
    for response in command:
        for key, value in response.items():
            if key == "time":
                try:
                    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except Exception as _:
                    print(f"Unable to parse time {value}")

    return None


def _read_csv(directory: str, message_type: DataMessageType, filter: List[DataMessageType]) -> np.ndarray:
    csv = np.empty([0, 10])  # 10 is the maximum number of columns expected for any data message
    string = np.empty([0, 1])

    if message_type not in filter:
        return csv, string

    file_path = os.path.join(directory, message_type.file_name)

    if not os.path.isfile(file_path):
        return csv, string

    try:
        csv = np.genfromtxt(file_path, delimiter=",", skip_header=1)

        if message_type in (DataMessageType.NOTIFICATION, DataMessageType.ERROR):
            string = np.genfromtxt(file_path, delimiter=",", skip_header=1, usecols=1, dtype=None, encoding=None)  # TODO: support strings containing commas
    except Exception as _:
        print(f"Unable to read file {file_path}")

    return csv, string


def _read_device(directory: str, filter: List[DataMessageType]) -> Device:
    command = _read_command(directory)

    interface, device_name, serial_number = _parse_ping(command)

    time = _parse_time(command)

    return Device(
        command,
        interface,
        device_name,
        serial_number,
        time,
        Inertial(*_read_csv(directory, DataMessageType.INERTIAL, filter)),
        Magnetometer(*_read_csv(directory, DataMessageType.MAGNETOMETER, filter)),
        Quaternion(*_read_csv(directory, DataMessageType.QUATERNION, filter)),
        RotationMatrix(*_read_csv(directory, DataMessageType.ROTATION_MATRIX, filter)),
        EulerAngles(*_read_csv(directory, DataMessageType.EULER_ANGLES, filter)),
        LinearAcceleration(*_read_csv(directory, DataMessageType.LINEAR_ACCELERATION, filter)),
        EarthAcceleration(*_read_csv(directory, DataMessageType.EARTH_ACCELERATION, filter)),
        AhrsStatus(*_read_csv(directory, DataMessageType.AHRS_STATUS, filter)),
        HighGAccelerometer(*_read_csv(directory, DataMessageType.HIGH_G_ACCELEROMETER, filter)),
        Temperature(*_read_csv(directory, DataMessageType.TEMPERATURE, filter)),
        Battery(*_read_csv(directory, DataMessageType.BATTERY, filter)),
        Rssi(*_read_csv(directory, DataMessageType.RSSI, filter)),
        SerialAccessory(*_read_csv(directory, DataMessageType.SERIAL_ACCESSORY, filter)),
        Notification(*_read_csv(directory, DataMessageType.NOTIFICATION, filter)),
        Error(*_read_csv(directory, DataMessageType.ERROR, filter)),
    )


def read(root: str, filter: List[DataMessageType] = None) -> List[Device]:
    if not os.path.isdir(root):
        raise Exception(f'"{root}" does not exist')

    if filter is None:
        filter = list(DataMessageType)

    device_directories = [os.path.join(root, d) for d in os.listdir(root) if not d.startswith(".")]

    if not device_directories:
        raise Exception(f'"{root}" is empty')

    return [_read_device(d, filter) for d in device_directories]
