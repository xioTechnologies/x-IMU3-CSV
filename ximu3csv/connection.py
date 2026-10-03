from collections.abc import Sequence
from dataclasses import dataclass, fields
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
class Connection:
    """Logged data of one connection.

    Each data message is an attribute named after its CSV file, e.g.
    `inertial` for Inertial.csv. A data message is empty if its file is not
    present or the data message was not read.

    Attributes
    ----------
    model
        Device model, or None if unknown.
    serial_number
        Device serial number, or None if unknown.
    device_name
        Device name, or None if unknown.
    config
        Connection configuration, or None if unknown.
    directory
        Name of the connection directory.
    command
        Responses read from Command.json.
    first_timestamp
        First timestamp of all data messages, or None if no data.
    last_timestamp
        Last timestamp of all data messages, or None if no data.
    """

    # Metadata.json
    model: str | None
    serial_number: str | None
    device_name: str | None
    config: str | None
    directory: str

    # Command.json
    command: list[dict[str, Any]]

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

    def __str__(self) -> str:
        return self.directory

    @cached_property
    def first_timestamp(self) -> float | None:
        """First timestamp of all data messages, or None if no data."""

        timestamps = [m.timestamp[0] for m in self._data_messages() if not m.is_empty]

        return min(timestamps) if timestamps else None

    @cached_property
    def last_timestamp(self) -> float | None:
        """Last timestamp of all data messages, or None if no data."""

        timestamps = [m.timestamp[-1] for m in self._data_messages() if not m.is_empty]

        return max(timestamps) if timestamps else None

    def get_response(self, key: str) -> Any:
        """Get the value of the response to a command key.

        Error responses are ignored. All other responses to the key must
        have the same value.

        Parameters
        ----------
        key
            Command key.

        Returns
        -------
        Any
            Response value.
        """

        responses = [c[key] for c in self.command if key in c]

        if not responses:
            raise RuntimeError(f"No response to {key!r} for {self}")

        values = [r for r in responses if not (isinstance(r, dict) and "error" in r)]

        if not values:
            raise RuntimeError(f"Error response to {key!r} for {self}: {responses[0]['error']}")

        if any(v != values[0] for v in values):
            raise RuntimeError(f"Conflicting responses to {key!r} for {self}: {values}")

        return values[0]

    def _data_messages(self) -> list[DataMessage]:
        return [getattr(self, f.name) for f in fields(self) if isinstance(getattr(self, f.name), DataMessage)]


def min_first_timestamp(connections: Sequence[Connection]) -> float | None:
    timestamps = [c.first_timestamp for c in connections if c.first_timestamp is not None]

    return min(timestamps) if timestamps else None


def max_last_timestamp(connections: Sequence[Connection]) -> float | None:
    timestamps = [c.last_timestamp for c in connections if c.last_timestamp is not None]

    return max(timestamps) if timestamps else None
