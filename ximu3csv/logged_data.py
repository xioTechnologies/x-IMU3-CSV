from collections.abc import Iterator
from dataclasses import dataclass, replace
from datetime import datetime
from functools import cached_property
from typing import Self, overload

from .connection import Connection


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
        timestamps = [c.first_timestamp for c in self._connections if c.first_timestamp is not None]

        return min(timestamps) if timestamps else None

    @cached_property
    def last_timestamp(self) -> float | None:
        timestamps = [c.last_timestamp for c in self._connections if c.last_timestamp is not None]

        return max(timestamps) if timestamps else None

    def _find(self, key: str) -> Connection:
        for attribute in ("serial_number", "device_name"):
            matches = [c for c in self._connections if getattr(c, attribute) == key]

            if len(matches) > 1:
                matches_string = "\n".join(f"{c.device_name} {c.serial_number}" for c in matches)

                raise RuntimeError(f"Multiple connections found for {key!r}:\n{matches_string}")

            if matches:
                return matches[0]

        raise KeyError(key)
