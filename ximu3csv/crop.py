from dataclasses import replace

from .data_messages import DataMessage
from .device import Device, update_first_and_last_timestamps


def _crop(message: DataMessage, start: int, stop: int) -> DataMessage:
    mask = (message.timestamp >= start) & (message.timestamp <= stop)

    return replace(
        message,
        _csv=message._csv[mask],
        _string=message._string[mask] if len(message._string) > 0 else message._string,
    )


def crop(devices: list[Device], start: int = 0, stop: int = 2**64 - 1) -> list[Device]:
    first_timestamps = [d.first_timestamp for d in devices if d.first_timestamp is not None]
    last_timestamps = [d.last_timestamp for d in devices if d.last_timestamp is not None]

    if not first_timestamps or not last_timestamps:
        return devices

    if start > max(last_timestamps):
        raise ValueError(f"Start is after last timestamp: {start} > {max(last_timestamps)}")

    if stop < min(first_timestamps):
        raise ValueError(f"Stop is before first timestamp: {stop} < {min(first_timestamps)}")

    devices = [
        replace(
            d,
            inertial=_crop(d.inertial, start, stop),
            magnetometer=_crop(d.magnetometer, start, stop),
            quaternion=_crop(d.quaternion, start, stop),
            rotation_matrix=_crop(d.rotation_matrix, start, stop),
            euler_angles=_crop(d.euler_angles, start, stop),
            linear_acceleration=_crop(d.linear_acceleration, start, stop),
            earth_acceleration=_crop(d.earth_acceleration, start, stop),
            ahrs_status=_crop(d.ahrs_status, start, stop),
            high_g_accelerometer=_crop(d.high_g_accelerometer, start, stop),
            temperature=_crop(d.temperature, start, stop),
            battery=_crop(d.battery, start, stop),
            rssi=_crop(d.rssi, start, stop),
            serial_accessory=_crop(d.serial_accessory, start, stop),
            notification=_crop(d.notification, start, stop),
            error=_crop(d.error, start, stop),
        )
        for d in devices
    ]

    return [update_first_and_last_timestamps(d) for d in devices]
