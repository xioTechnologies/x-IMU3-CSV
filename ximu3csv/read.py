import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import Any

from .connection import Connection
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
from .logged_data import LoggedData
from .metadata import read_metadata


def read(path: Path | str, data_message_type: DataMessageType = DataMessageType.ALL) -> LoggedData:
    path = Path(path).absolute()

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    metadata = read_metadata(path)

    if metadata is not None:
        return LoggedData(
            metadata.name,
            metadata.time,
            tuple(
                replace(
                    _read_connection(path / c.directory, data_message_type),
                    model=c.model,
                    serial_number=c.serial_number,
                    device_name=c.device_name,
                    config=c.config,
                )
                for c in metadata.connections
            ),
        )

    connection_directories = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]

    if not connection_directories:
        raise FileNotFoundError(f"No connection directories found: {path}")

    connections = tuple(_read_connection(d, data_message_type) for d in connection_directories)

    ping_responses = tuple(_get_ping_response(c.command) for c in connections)

    times = tuple(_get_time(c.command) for c in connections)

    return LoggedData(
        path.name,
        max((t for t in times if t is not None), default=None),
        tuple(
            replace(
                c,
                model=m,
                serial_number=s,
                device_name=d,
            )
            for c, (m, s, d) in zip(connections, ping_responses)
        ),
    )


def _read_connection(directory: Path, data_message_type: DataMessageType) -> Connection:
    if not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    return Connection(
        None,
        None,
        None,
        None,
        _read_command(directory),
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
    )


def _read_command(directory: Path) -> list[dict[str, Any]]:
    file_path = directory / "Command.json"

    if not file_path.is_file():
        return []

    try:
        with file_path.open(encoding="utf-8") as file:
            return json.load(file)
    except Exception as exception:
        exception.add_note(f"Unable to read file: {file_path}")
        raise


def _read_data_message(directory: Path, data_message: type[DataMessage], flag: DataMessageType, data_message_type: DataMessageType) -> DataMessage:
    if flag not in data_message_type:
        return data_message._empty()

    return data_message._read(directory)


def _get_ping_response(command: list[dict[str, Any]]) -> tuple[str | None, str | None, str | None]:
    for response in command:
        if "ping" in response:
            ping = response["ping"]

            return ping.get("model"), ping.get("sn"), ping.get("name")

    return None, None, None


def _get_time(command: list[dict[str, Any]]) -> datetime | None:
    for response in command:
        if "time" in response:
            return datetime.strptime(response["time"], "%Y-%m-%d %H:%M:%S")

    return None
