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
    DataMessageFlag,
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


def read(path: Path | str, data_messages: DataMessageFlag = DataMessageFlag.ALL) -> LoggedData:
    """Read data written by the x-IMU3 data logger or file converter.

    If the directory contains Metadata.json then connections are read in
    the order listed. Otherwise, each subdirectory is read as a connection,
    in alphabetical order.

    Parameters
    ----------
    path
        Logged data directory.
    data_messages
        Data messages to read. Data messages not included are empty.

    Returns
    -------
    LoggedData
        Logged data.
    """

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
                    _read_connection(path / c.directory, data_messages),
                    model=c.model,
                    serial_number=c.serial_number,
                    device_name=c.device_name,
                    config=c.config,
                )
                for c in metadata.connections
            ),
        )

    connection_directories = [d for d in sorted(path.iterdir()) if d.is_dir() and not d.name.startswith(".")]

    if not connection_directories:
        raise FileNotFoundError(f"No connection directories found: {path}")

    connections = tuple(_read_connection(d, data_messages) for d in connection_directories)

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


def _read_connection(directory: Path, data_messages: DataMessageFlag) -> Connection:
    if not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    return Connection(
        None,
        None,
        None,
        None,
        directory.name,
        _read_command(directory),
        _read_data_message(directory, Inertial, DataMessageFlag.INERTIAL, data_messages),
        _read_data_message(directory, Magnetometer, DataMessageFlag.MAGNETOMETER, data_messages),
        _read_data_message(directory, HighGAccelerometer, DataMessageFlag.HIGH_G_ACCELEROMETER, data_messages),
        _read_data_message(directory, Quaternion, DataMessageFlag.QUATERNION, data_messages),
        _read_data_message(directory, RotationMatrix, DataMessageFlag.ROTATION_MATRIX, data_messages),
        _read_data_message(directory, EulerAngles, DataMessageFlag.EULER_ANGLES, data_messages),
        _read_data_message(directory, LinearAcceleration, DataMessageFlag.LINEAR_ACCELERATION, data_messages),
        _read_data_message(directory, EarthAcceleration, DataMessageFlag.EARTH_ACCELERATION, data_messages),
        _read_data_message(directory, AhrsStatus, DataMessageFlag.AHRS_STATUS, data_messages),
        _read_data_message(directory, SerialAccessory, DataMessageFlag.SERIAL_ACCESSORY, data_messages),
        _read_data_message(directory, Sync, DataMessageFlag.SYNC, data_messages),
        _read_data_message(directory, Ltc, DataMessageFlag.LTC, data_messages),
        _read_data_message(directory, Temperature, DataMessageFlag.TEMPERATURE, data_messages),
        _read_data_message(directory, Battery, DataMessageFlag.BATTERY, data_messages),
        _read_data_message(directory, Rssi, DataMessageFlag.RSSI, data_messages),
        _read_data_message(directory, Button, DataMessageFlag.BUTTON, data_messages),
        _read_data_message(directory, Notification, DataMessageFlag.NOTIFICATION, data_messages),
        _read_data_message(directory, Error, DataMessageFlag.ERROR, data_messages),
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


def _read_data_message(directory: Path, data_message_type: type[DataMessage], flag: DataMessageFlag, data_messages: DataMessageFlag) -> DataMessage:
    if flag not in data_messages:
        return data_message_type._empty()

    return data_message_type._read(directory)


def _get_ping_response(command: list[dict[str, Any]]) -> tuple[str | None, str | None, str | None]:
    pings = [c["ping"] for c in command if "ping" in c]

    if not pings or not isinstance(pings[0], dict):
        return None, None, None

    return pings[0].get("model"), pings[0].get("sn"), pings[0].get("name")


def _get_time(command: list[dict[str, Any]]) -> datetime | None:
    times = [c["time"] for c in command if "time" in c]

    if not times or not isinstance(times[0], str):
        return None

    return datetime.strptime(times[0], "%Y-%m-%d %H:%M:%S")
