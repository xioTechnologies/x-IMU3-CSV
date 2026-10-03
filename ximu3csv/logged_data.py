from collections.abc import Iterator
from dataclasses import dataclass, replace
from datetime import datetime
from functools import cached_property
from typing import Self, overload

from .connection import Connection, max_last_timestamp, min_first_timestamp
from .post_processing import (
    create_acceleration,
    create_euler_angles,
    create_quaternion,
    create_rotation_matrix,
    offset_timestamps,
    resample,
    set_heading,
    sync,
    truncate,
)
from .post_processing.sync import EdgePolarity


@dataclass(frozen=True)
class LoggedData:
    """Logged data of one or more connections.

    Connections are accessed by index, slice, or key. A key matches the
    directory, config, serial number, device name, or model of a
    connection, in that order.

    Attributes
    ----------
    name
        Name of the logged data.
    time
        Time at which logging started, or None if unknown.
    first_timestamp
        First timestamp of all connections, or None if no data.
    last_timestamp
        Last timestamp of all connections, or None if no data.
    """

    name: str
    time: datetime | None

    _connections: tuple[Connection, ...]

    @overload
    def __getitem__(self, key: int) -> Connection: ...

    @overload
    def __getitem__(self, key: slice) -> Self: ...

    @overload
    def __getitem__(self, key: str) -> Connection: ...

    def __getitem__(self, key: int | slice | str) -> Connection | Self:
        if isinstance(key, slice):
            return replace(self, _connections=self._connections[key])

        if isinstance(key, str):
            return self._find(key)

        return self._connections[key]

    def __len__(self) -> int:
        return len(self._connections)

    def __iter__(self) -> Iterator[Connection]:
        return iter(self._connections)

    @cached_property
    def first_timestamp(self) -> float | None:
        """First timestamp of all connections, or None if no data."""

        return min_first_timestamp(self._connections)

    @cached_property
    def last_timestamp(self) -> float | None:
        """Last timestamp of all connections, or None if no data."""

        return max_last_timestamp(self._connections)

    def truncate(self, before: float | None = None, after: float | None = None) -> Self:
        """Truncate data to a timestamp range.

        `before` and `after` are inclusive.

        Parameters
        ----------
        before
            Timestamp (us) before which data is removed, or None to keep
            the start.
        after
            Timestamp (us) after which data is removed, or None to keep the
            end.

        Returns
        -------
        LoggedData
            Truncated data.
        """

        return replace(self, _connections=truncate.truncate(self._connections, before, after))

    def sync_start(self, polarity: EdgePolarity, index: int = 0) -> Self:
        """Truncate data before the sync edge.

        Parameters
        ----------
        polarity
            Polarity of the edge.
        index
            Index of the edge, counting only edges of the polarity given by
            `polarity`. Negative indices count from the last edge.

        Returns
        -------
        LoggedData
            Truncated data.
        """

        return replace(self, _connections=sync.sync_start(self._connections, polarity, index))

    def sync_end(self, polarity: EdgePolarity, index: int = 0) -> Self:
        """Truncate data after the sync edge.

        Parameters
        ----------
        polarity
            Polarity of the edge.
        index
            Index of the edge, counting only edges of the polarity given by
            `polarity`. Negative indices count from the last edge.

        Returns
        -------
        LoggedData
            Truncated data.
        """

        return replace(self, _connections=sync.sync_end(self._connections, polarity, index))

    def offset_timestamps(self, offset: float) -> Self:
        """Add a constant to all timestamps.

        Parameters
        ----------
        offset
            Offset (us).

        Returns
        -------
        LoggedData
            Data with offset timestamps.
        """

        return replace(self, _connections=offset_timestamps.offset_timestamps(self._connections, offset))

    def zero_timestamps(self) -> Self:
        """Offset timestamps to start at zero.

        Returns
        -------
        LoggedData
            Data with zeroed timestamps.
        """

        return replace(self, _connections=offset_timestamps.zero_timestamps(self._connections))

    def resample(self, sample_rate: float) -> Self:
        """Resample data over the span of all connections.

        Values are held beyond the span of each message. Event messages are
        not resampled and battery charging status is NaN.

        Parameters
        ----------
        sample_rate
            Sample rate (Hz).

        Returns
        -------
        LoggedData
            Resampled data.
        """

        return replace(self, _connections=resample.resample(self._connections, sample_rate))

    def set_heading(self, heading: float, timestamp: float | None = None) -> Self:
        """Set the heading.

        The heading is set to `heading` at the timestamp and subsequent
        data is offset by the same amount. Earth acceleration data messages
        are not updated.

        Parameters
        ----------
        heading
            Heading (degrees).
        timestamp
            Timestamp (us) at which the heading is set, or None for the
            first sample.

        Returns
        -------
        LoggedData
            Data with the heading set.
        """

        return replace(self, _connections=set_heading.set_heading(self._connections, heading, timestamp))

    def zero_heading(self, timestamp: float | None = None) -> Self:
        """Zero the heading.

        The heading is set to zero at the timestamp and subsequent data is
        offset by the same amount. Earth acceleration data messages are not
        updated.

        Parameters
        ----------
        timestamp
            Timestamp (us) at which the heading is set, or None for the
            first sample.

        Returns
        -------
        LoggedData
            Data with the heading zeroed.
        """

        return replace(self, _connections=set_heading.zero_heading(self._connections, timestamp))

    def create_quaternion(self) -> Self:
        """Create quaternion data messages.

        Created where missing, from rotation matrix or Euler angles data
        messages.

        Returns
        -------
        LoggedData
            Data with quaternion data messages.
        """

        return replace(self, _connections=create_quaternion.create_quaternion(self._connections))

    def create_rotation_matrix(self) -> Self:
        """Create rotation matrix data messages.

        Created where missing, from quaternion or Euler angles data
        messages.

        Returns
        -------
        LoggedData
            Data with rotation matrix data messages.
        """

        return replace(self, _connections=create_rotation_matrix.create_rotation_matrix(self._connections))

    def create_euler_angles(self) -> Self:
        """Create Euler angles data messages.

        Created where missing, from quaternion or rotation matrix data
        messages.

        Returns
        -------
        LoggedData
            Data with Euler angles data messages.
        """

        return replace(self, _connections=create_euler_angles.create_euler_angles(self._connections))

    def create_linear_acceleration(self, z_up: bool = True) -> Self:
        """Create linear acceleration data messages.

        Created where missing, from inertial and orientation data messages.

        Parameters
        ----------
        z_up
            True for NWU and ENU earth axis conventions. False for NED.

        Returns
        -------
        LoggedData
            Data with linear acceleration data messages.
        """

        return replace(self, _connections=create_acceleration.create_linear_acceleration(self._connections, z_up))

    def create_earth_acceleration(self, z_up: bool = True) -> Self:
        """Create earth acceleration data messages.

        Created where missing, from inertial and orientation data messages.

        Parameters
        ----------
        z_up
            True for NWU and ENU earth axis conventions. False for NED.

        Returns
        -------
        LoggedData
            Data with earth acceleration data messages.
        """

        return replace(self, _connections=create_acceleration.create_earth_acceleration(self._connections, z_up))

    def _find(self, key: str) -> Connection:
        for attribute in ("directory", "config", "serial_number", "device_name", "model"):  # descending order of uniqueness
            matches = [c for c in self._connections if getattr(c, attribute) == key]

            if len(matches) > 1:
                matches_string = "\n".join(str(c) for c in matches)

                raise RuntimeError(f"Multiple connections found for {key!r}:\n{matches_string}")

            if matches:
                return matches[0]

        raise KeyError(key)
