import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .data_messages import (
    AhrsStatus,
    Battery,
    Button,
    DataMessage,
    DataMessageType,
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
from .device import Device, update_first_and_last_timestamps


def _read_command(directory: Path) -> list[dict[str, Any]]:
    file_path = directory / "Command.json"

    if not file_path.is_file():
        return []

    with file_path.open(encoding="utf-8") as file:
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


def _read_data_message(directory: Path, data_message: type[DataMessage], flag: DataMessageType, data_message_type: DataMessageType) -> DataMessage:
    if flag not in data_message_type:
        return data_message._empty()

    return data_message._read(directory)


def _read_device(directory: Path, data_message_type: DataMessageType) -> Device:
    command = _read_command(directory)

    interface, device_name, serial_number = _parse_ping(command)

    time = _parse_time(command)

    device = Device(
        command,
        interface,
        device_name,
        serial_number,
        time,
        _read_data_message(directory, Inertial, DataMessageType.INERTIAL, data_message_type),
        _read_data_message(directory, Magnetometer, DataMessageType.MAGNETOMETER, data_message_type),
        _read_data_message(directory, HighGAccelerometer, DataMessageType.HIGH_G_ACCELEROMETER, data_message_type),
        _read_data_message(directory, Quaternion, DataMessageType.QUATERNION, data_message_type),
        _read_data_message(directory, RotationMatrix, DataMessageType.ROTATION_MATRIX, data_message_type),
        _read_data_message(directory, EulerAngles, DataMessageType.EULER_ANGLES, data_message_type),
        _read_data_message(directory, LinearAcceleration, DataMessageType.LINEAR_ACCELERATION, data_message_type),
        _read_data_message(directory, EarthAcceleration, DataMessageType.EARTH_ACCELERATION, data_message_type),
        _read_data_message(directory, AhrsStatus, DataMessageType.AHRS_STATUS, data_message_type),
        _read_data_message(directory, SerialAccessory, DataMessageType.SERIAL_ACCESSORY, data_message_type),
        _read_data_message(directory, Sync, DataMessageType.SYNC, data_message_type),
        _read_data_message(directory, Ltc, DataMessageType.LTC, data_message_type),
        _read_data_message(directory, Temperature, DataMessageType.TEMPERATURE, data_message_type),
        _read_data_message(directory, Battery, DataMessageType.BATTERY, data_message_type),
        _read_data_message(directory, Rssi, DataMessageType.RSSI, data_message_type),
        _read_data_message(directory, Button, DataMessageType.BUTTON, data_message_type),
        _read_data_message(directory, Notification, DataMessageType.NOTIFICATION, data_message_type),
        _read_data_message(directory, Error, DataMessageType.ERROR, data_message_type),
        None,
        None,
    )

    return update_first_and_last_timestamps(device)


def read(path: Path | str, data_message_type: DataMessageType = DataMessageType.ALL) -> list[Device]:
    path = Path(path).absolute()

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    device_directories = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]

    if not device_directories:
        raise FileNotFoundError(f"No device directories found: {path}")

    return [_read_device(d, data_message_type) for d in device_directories]
