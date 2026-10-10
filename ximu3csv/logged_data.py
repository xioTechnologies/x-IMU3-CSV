from collections.abc import Iterator
from dataclasses import dataclass, replace
from datetime import datetime
from functools import cached_property
from typing import Self, overload

from .connection import Connection, max_last_timestamp, min_first_timestamp
from .post_processing import calculate_euler_angles, calculate_quaternion, calculate_rotation_matrix, crop, offset_timestamps, resample, set_heading


@dataclass(frozen=True)
class LoggedData:
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
        return min_first_timestamp(self._connections)

    @cached_property
    def last_timestamp(self) -> float | None:
        return max_last_timestamp(self._connections)

    def crop(self, start: float | None = None, stop: float | None = None) -> Self:
        return replace(self, _connections=crop.crop(self._connections, start, stop))

    def offset_timestamps(self, offset: float) -> Self:
        return replace(self, _connections=offset_timestamps.offset_timestamps(self._connections, offset))

    def zero_timestamps(self) -> Self:
        return replace(self, _connections=offset_timestamps.zero_timestamps(self._connections))

    def resample(self, sample_rate: float) -> Self:
        return replace(self, _connections=resample.resample(self._connections, sample_rate))

    def set_heading(self, heading: float, timestamp: float | None = None) -> Self:
        return replace(self, _connections=set_heading.set_heading(self._connections, heading, timestamp))

    def zero_heading(self, timestamp: float | None = None) -> Self:
        return replace(self, _connections=set_heading.zero_heading(self._connections, timestamp))

    def calculate_quaternion(self) -> Self:
        return replace(self, _connections=calculate_quaternion.calculate_quaternion(self._connections))

    def calculate_rotation_matrix(self) -> Self:
        return replace(self, _connections=calculate_rotation_matrix.calculate_rotation_matrix(self._connections))

    def calculate_euler_angles(self) -> Self:
        return replace(self, _connections=calculate_euler_angles.calculate_euler_angles(self._connections))

    def _find(self, key: str) -> Connection:
        for attribute in ("config", "serial_number", "device_name", "model"):
            matches = [c for c in self._connections if getattr(c, attribute) == key]

            if len(matches) > 1:
                matches_string = "\n".join(f"{c.model!r}, {c.serial_number!r}, {c.device_name!r}, {c.config!r}" for c in matches)

                raise RuntimeError(f"Multiple connections found for {key!r}:\n{matches_string}")

            if matches:
                return matches[0]

        raise KeyError(key)
