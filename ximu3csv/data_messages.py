from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Flag, auto
from pathlib import Path
from typing import Self

import numpy as np


class DataMessageType(Flag):
    INERTIAL = auto()
    MAGNETOMETER = auto()
    HIGH_G_ACCELEROMETER = auto()
    QUATERNION = auto()
    ROTATION_MATRIX = auto()
    EULER_ANGLES = auto()
    LINEAR_ACCELERATION = auto()
    EARTH_ACCELERATION = auto()
    AHRS_STATUS = auto()
    SERIAL_ACCESSORY = auto()
    SYNC = auto()
    LTC = auto()
    TEMPERATURE = auto()
    BATTERY = auto()
    RSSI = auto()
    BUTTON = auto()
    NOTIFICATION = auto()
    ERROR = auto()

    ALL = INERTIAL | MAGNETOMETER | HIGH_G_ACCELEROMETER | QUATERNION | ROTATION_MATRIX | EULER_ANGLES | LINEAR_ACCELERATION | EARTH_ACCELERATION | AHRS_STATUS | SERIAL_ACCESSORY | SYNC | LTC | TEMPERATURE | BATTERY | RSSI | BUTTON | NOTIFICATION | ERROR


@dataclass(frozen=True)
class DataMessage(ABC):
    @property
    @abstractmethod
    def timestamp(self) -> np.ndarray:
        pass

    @classmethod
    @abstractmethod
    def _read(cls, device_path: Path) -> Self:
        pass

    @classmethod
    @abstractmethod
    def _empty(cls) -> Self:
        pass


@dataclass(frozen=True)
class FloatMessage(DataMessage):
    _csv: np.ndarray

    @property
    def timestamp(self) -> np.ndarray:
        return self._csv[:, 0]

    @classmethod
    def _read(cls, device_path: Path) -> Self:
        file_path = device_path / f"{cls.__name__}.csv"

        if not file_path.is_file():
            return cls._empty()

        try:
            return cls(np.genfromtxt(file_path, delimiter=",", skip_header=1, ndmin=2))
        except Exception as exception:
            exception.add_note(f"Unable to read file: {file_path}")
            raise


@dataclass(frozen=True)
class CharArrayMessage(DataMessage):
    _timestamp: np.ndarray
    _string: np.ndarray

    @property
    def timestamp(self) -> np.ndarray:
        return self._timestamp

    @property
    def string(self) -> np.ndarray:
        return self._string

    @classmethod
    def _read(cls, device_path: Path) -> Self:
        file_path = device_path / f"{cls.__name__}.csv"

        if not file_path.is_file():
            return cls._empty()

        try:
            with file_path.open(encoding="utf-8") as file:
                next(file)  # skip headings

                rows = [line.rstrip("\n").split(",", 1) for line in file]

            return cls(np.array([float(r[0]) for r in rows]), np.array([r[1] for r in rows], dtype=str))
        except Exception as exception:
            exception.add_note(f"Unable to read file: {file_path}")
            raise

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty(0), np.empty(0, dtype=str))


@dataclass(frozen=True)
class Inertial(FloatMessage):
    @property
    def gyroscope_xyz(self) -> np.ndarray:
        return self._csv[:, 1:4]

    @property
    def gyroscope_x(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def gyroscope_y(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def gyroscope_z(self) -> np.ndarray:
        return self._csv[:, 3]

    @property
    def accelerometer_xyz(self) -> np.ndarray:
        return self._csv[:, 4:7]

    @property
    def accelerometer_x(self) -> np.ndarray:
        return self._csv[:, 4]

    @property
    def accelerometer_y(self) -> np.ndarray:
        return self._csv[:, 5]

    @property
    def accelerometer_z(self) -> np.ndarray:
        return self._csv[:, 6]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 7]))


@dataclass(frozen=True)
class Magnetometer(FloatMessage):
    @property
    def xyz(self) -> np.ndarray:
        return self._csv[:, 1:4]

    @property
    def x(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def y(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def z(self) -> np.ndarray:
        return self._csv[:, 3]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 4]))


@dataclass(frozen=True)
class HighGAccelerometer(FloatMessage):
    @property
    def xyz(self) -> np.ndarray:
        return self._csv[:, 1:4]

    @property
    def x(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def y(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def z(self) -> np.ndarray:
        return self._csv[:, 3]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 4]))


@dataclass(frozen=True)
class Quaternion(FloatMessage):
    @property
    def wxyz(self) -> np.ndarray:
        return self._csv[:, 1:5]

    @property
    def w(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def x(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def y(self) -> np.ndarray:
        return self._csv[:, 3]

    @property
    def z(self) -> np.ndarray:
        return self._csv[:, 4]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 5]))


@dataclass(frozen=True)
class RotationMatrix(FloatMessage):
    @property
    def xx_to_zz(self) -> np.ndarray:
        return self._csv[:, 1:10]

    @property
    def xx(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def xy(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def xz(self) -> np.ndarray:
        return self._csv[:, 3]

    @property
    def yx(self) -> np.ndarray:
        return self._csv[:, 4]

    @property
    def yy(self) -> np.ndarray:
        return self._csv[:, 5]

    @property
    def yz(self) -> np.ndarray:
        return self._csv[:, 6]

    @property
    def zx(self) -> np.ndarray:
        return self._csv[:, 7]

    @property
    def zy(self) -> np.ndarray:
        return self._csv[:, 8]

    @property
    def zz(self) -> np.ndarray:
        return self._csv[:, 9]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 10]))


@dataclass(frozen=True)
class EulerAngles(FloatMessage):
    @property
    def roll_pitch_yaw(self) -> np.ndarray:
        return self._csv[:, 1:4]

    @property
    def roll(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def pitch(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def yaw(self) -> np.ndarray:
        return self._csv[:, 3]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 4]))


@dataclass(frozen=True)
class LinearAcceleration(FloatMessage):
    @property
    def xyz(self) -> np.ndarray:
        return self._csv[:, 1:4]

    @property
    def x(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def y(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def z(self) -> np.ndarray:
        return self._csv[:, 3]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 4]))


@dataclass(frozen=True)
class EarthAcceleration(FloatMessage):
    @property
    def xyz(self) -> np.ndarray:
        return self._csv[:, 1:4]

    @property
    def x(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def y(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def z(self) -> np.ndarray:
        return self._csv[:, 3]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 4]))


@dataclass(frozen=True)
class AhrsStatus(CharArrayMessage):
    pass


@dataclass(frozen=True)
class SerialAccessory(CharArrayMessage):
    pass


@dataclass(frozen=True)
class Sync(FloatMessage):
    @property
    def edge(self) -> np.ndarray:
        return self._csv[:, 1]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 2]))


@dataclass(frozen=True)
class Ltc(CharArrayMessage):
    pass


@dataclass(frozen=True)
class Temperature(FloatMessage):
    @property
    def temperature(self) -> np.ndarray:
        return self._csv[:, 1]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 2]))


@dataclass(frozen=True)
class Battery(FloatMessage):
    @property
    def percentage(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def voltage(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def charging_status(self) -> np.ndarray:
        return self._csv[:, 3]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 4]))


@dataclass(frozen=True)
class Rssi(FloatMessage):
    @property
    def percentage(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def power(self) -> np.ndarray:
        return self._csv[:, 2]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 3]))


@dataclass(frozen=True)
class Button(FloatMessage):
    @property
    def state(self) -> np.ndarray:
        return self._csv[:, 1]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 2]))


@dataclass(frozen=True)
class Notification(CharArrayMessage):
    pass


@dataclass(frozen=True)
class Error(CharArrayMessage):
    pass
