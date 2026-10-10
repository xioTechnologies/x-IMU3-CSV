import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Connection:
    model: str
    serial_number: str
    device_name: str
    config: str
    directory: str


@dataclass(frozen=True)
class Metadata:
    name: str
    time: datetime
    connections: tuple[Connection, ...]


def read_metadata(path: Path) -> Metadata | None:
    file_path = path / "Metadata.json"

    if not file_path.is_file():
        return None

    try:
        with file_path.open(encoding="utf-8") as file:
            metadata = json.load(file)

        return Metadata(
            metadata["name"],
            datetime.strptime(metadata["time"], "%Y-%m-%d %H:%M:%S"),
            tuple(
                Connection(
                    c["model"],
                    c["serial_number"],
                    c["device_name"],
                    c["config"],
                    c["directory"],
                )
                for c in metadata["connections"]
            ),
        )
    except Exception as exception:
        exception.add_note(f"Unable to read file: {file_path}")
        raise
