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


# let metadata = serde_json::json!({
#     "name": name,
#     "time": std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs().to_string(), // TODO: use YYYY-MM-DD hh:mm:ss
#     "connections": connections.iter().zip(directories.iter()).map(|(connection, directory)| {
#         let ping_response = connection.internal.lock().unwrap().get_receiver().lock().unwrap().dispatcher.ping_response.lock().unwrap().clone();
#         let config = connection.internal.lock().unwrap().get_config();

#         serde_json::json!({
#             "model": "", // TODO: use model from ping_response
#             "serial_number": ping_response.as_ref().map(|ping_response| ping_response.serial_number.clone()).unwrap_or_default(),
#             "device_name": ping_response.as_ref().map(|ping_response| ping_response.device_name.clone()).unwrap_or_default(),
#             "config": config.to_string(),
#             "directory": directory,
#         })
#     }).collect::<Vec<_>>(),
# });

# std::fs::write(root.join("Metadata.json"), serde_json::to_string_pretty(&metadata).unwrap())?;
