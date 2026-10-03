import json
from datetime import datetime
from pathlib import Path
from typing import Any

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


def _read_command(directory: Path) -> list[dict[str, Any]]:
    file_path = directory / "Command.json"

    if not file_path.is_file():
        return []

    with file_path.open() as file:
        return json.load(file)


def _parse_ping(command: list[dict[str, Any]]) -> tuple[str | None, str | None, str | None]:
    for response in command:
        for key, value in response.items():
            if key == "ping":
                try:
                    return value["interface"], value["name"], value["sn"]
                except Exception:
                    print(f"Unable to parse ping response: {value}")

    return None, None, None


def _parse_time(command: list[dict[str, Any]]) -> datetime | None:
    for response in command:
        for key, value in response.items():
            if key == "time":
                try:
                    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    print(f"Unable to parse time: {value}")

    return None


def _read_csv(directory: Path, message_type: DataMessageType, filter: tuple[DataMessageType, ...]) -> tuple[np.ndarray, np.ndarray]:
    csv = np.empty([0, 10])  # 10 is the maximum number of columns expected for any data message
    string = np.empty([0, 1])

    if message_type not in filter:
        return csv, string

    file_path = directory / message_type.file_name

    if not file_path.is_file():
        return csv, string

    try:
        csv = np.genfromtxt(file_path, delimiter=",", skip_header=1, ndmin=2)

        if message_type in (DataMessageType.NOTIFICATION, DataMessageType.ERROR):
            string = np.genfromtxt(file_path, delimiter=",", skip_header=1, usecols=(1,), dtype=None, encoding="utf-8")  # TODO: support strings containing commas
    except Exception:
        print(f"Unable to read file: {file_path}")

    return csv, string


def _read_device(directory: Path, filter: tuple[DataMessageType, ...]) -> Device:
    command = _read_command(directory)

    interface, device_name, serial_number = _parse_ping(command)

    time = _parse_time(command)

    device = Device(
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
        None,
        None,
    )

    return update_first_and_last_timestamps(device)


def read(path: Path | str, filter: DataMessageType | tuple[DataMessageType, ...] = tuple(DataMessageType)) -> list[Device]:
    path = Path(path).absolute()

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    if isinstance(filter, DataMessageType):
        filter = (filter,)

    device_directories = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]

    if not device_directories:
        raise FileNotFoundError(f"No device directories found: {path}")

    return [_read_device(d, filter) for d in device_directories]
