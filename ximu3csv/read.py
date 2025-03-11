import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

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
from .device import Device, update_first_and_last_timestamps


def __read_command(directory: str) -> List[Dict[str, Any]]:
    file_path = os.path.join(directory, "Command.json")

    if not os.path.isfile(file_path):
        return []

    with open(file_path) as file:
        return json.load(file)


def __parse_ping(command: List[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    for response in command:
        for key, value in response.items():
            if key == "ping":
                try:
                    return value["interface"], value["name"], value["sn"]
                except Exception as _:
                    print(f"Unable to parse ping response {value}")

    return None, None, None


def __parse_time(command: List[Dict[str, Any]]) -> Optional[datetime]:
    for response in command:
        for key, value in response.items():
            if key == "time":
                try:
                    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except Exception as _:
                    print(f"Unable to parse time {value}")

    return None


def __read_csv(directory: str, message_type: DataMessageType, filter: Tuple[DataMessageType, ...]) -> np.ndarray:
    csv = np.empty([0, 10])  # 10 is the maximum number of columns expected for any data message
    string = np.empty([0, 1])

    if message_type not in filter:
        return csv, string

    file_path = os.path.join(directory, message_type.file_name)

    if not os.path.isfile(file_path):
        return csv, string

    try:
        csv = np.genfromtxt(file_path, delimiter=",", skip_header=1, ndmin=2)

        if message_type in (DataMessageType.NOTIFICATION, DataMessageType.ERROR):
            string = np.genfromtxt(file_path, delimiter=",", skip_header=1, ndmin=2, usecols=1, dtype=None, encoding=None)  # TODO: support strings containing commas
    except Exception as _:
        print(f"Unable to read file {file_path}")

    return csv, string


def __read_device(directory: str, filter: Tuple[DataMessageType, ...]) -> Device:
    command = __read_command(directory)

    interface, device_name, serial_number = __parse_ping(command)

    time = __parse_time(command)

    device = Device(
        command,
        interface,
        device_name,
        serial_number,
        time,
        Inertial(*__read_csv(directory, DataMessageType.INERTIAL, filter)),
        Magnetometer(*__read_csv(directory, DataMessageType.MAGNETOMETER, filter)),
        Quaternion(*__read_csv(directory, DataMessageType.QUATERNION, filter)),
        RotationMatrix(*__read_csv(directory, DataMessageType.ROTATION_MATRIX, filter)),
        EulerAngles(*__read_csv(directory, DataMessageType.EULER_ANGLES, filter)),
        LinearAcceleration(*__read_csv(directory, DataMessageType.LINEAR_ACCELERATION, filter)),
        EarthAcceleration(*__read_csv(directory, DataMessageType.EARTH_ACCELERATION, filter)),
        AhrsStatus(*__read_csv(directory, DataMessageType.AHRS_STATUS, filter)),
        HighGAccelerometer(*__read_csv(directory, DataMessageType.HIGH_G_ACCELEROMETER, filter)),
        Temperature(*__read_csv(directory, DataMessageType.TEMPERATURE, filter)),
        Battery(*__read_csv(directory, DataMessageType.BATTERY, filter)),
        Rssi(*__read_csv(directory, DataMessageType.RSSI, filter)),
        SerialAccessory(*__read_csv(directory, DataMessageType.SERIAL_ACCESSORY, filter)),
        Notification(*__read_csv(directory, DataMessageType.NOTIFICATION, filter)),
        Error(*__read_csv(directory, DataMessageType.ERROR, filter)),
        None,
        None,
    )

    return update_first_and_last_timestamps(device)


def read(root: str, filter: Union[DataMessageType, Tuple[DataMessageType, ...]] = tuple(DataMessageType)) -> List[Device]:
    if not os.path.isdir(root):
        raise ValueError(f'"{root}" does not exist')

    if isinstance(filter, DataMessageType):
        filter = (filter,)

    device_directories = [os.path.join(root, d) for d in os.listdir(root) if not d.startswith(".")]

    if not device_directories:
        raise ValueError(f'"{root}" is empty')

    return [__read_device(d, filter) for d in device_directories]
