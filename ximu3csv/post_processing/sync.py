from collections.abc import Sequence
from enum import Enum, auto

from ..connection import Connection
from . import truncate


class EdgePolarity(Enum):
    RISING = auto()
    FALLING = auto()


def sync_start(connections: Sequence[Connection], polarity: EdgePolarity, index: int) -> tuple[Connection, ...]:
    return truncate.truncate(connections, _get_edge(connections, polarity, index), None)


def sync_end(connections: Sequence[Connection], polarity: EdgePolarity, index: int) -> tuple[Connection, ...]:
    return truncate.truncate(connections, None, _get_edge(connections, polarity, index))


def _get_edge(connections: Sequence[Connection], polarity: EdgePolarity, index: int) -> float:
    sync_connections = [c for c in connections if not c.sync.is_empty]

    if not sync_connections:
        raise ValueError("No sync")

    if len(sync_connections) > 1:
        sync_connections_string = "\n".join(str(s) for s in sync_connections)

        raise ValueError(f"Multiple connections with sync:\n{sync_connections_string}")

    sync = sync_connections[0].sync

    edges = sync.rising_edge if polarity is EdgePolarity.RISING else sync.falling_edge

    if (index >= len(edges)) or (index < -len(edges)):
        raise ValueError(f"No {polarity.name.lower()} edge at index: {index}")

    return float(edges[index])
