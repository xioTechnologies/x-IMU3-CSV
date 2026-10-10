from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Flag, auto
from pathlib import Path
from typing import ClassVar, Self

import numpy as np
import scipy


class DataMessageFlag(Flag):
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
    _file_name: ClassVar[str]

    @property
    @abstractmethod
    def timestamp(self) -> np.ndarray:
        pass

    @property
    def is_empty(self) -> bool:
        return len(self.timestamp) == 0

    @classmethod
    @abstractmethod
    def _read(cls, connection_path: Path) -> Self:
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
    def _read(cls, connection_path: Path) -> Self:
        file_path = connection_path / cls._file_name

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
    def _read(cls, connection_path: Path) -> Self:
        file_path = connection_path / cls._file_name

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
class OrientationMessage(FloatMessage):
    @abstractmethod
    def _to_rotations(self) -> scipy.spatial.transform.Rotation:
        pass

    @classmethod
    @abstractmethod
    def _from_rotations(cls, timestamp: np.ndarray, rotations: scipy.spatial.transform.Rotation) -> Self:
        pass


@dataclass(frozen=True)
class Inertial(FloatMessage):
    _file_name = "Inertial.csv"

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
    _file_name = "Magnetometer.csv"

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
    _file_name = "HighGAccelerometer.csv"

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
class Quaternion(OrientationMessage):
    _file_name = "Quaternion.csv"

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

    def _to_rotations(self) -> scipy.spatial.transform.Rotation:
        return scipy.spatial.transform.Rotation.from_quat(self.wxyz[:, [1, 2, 3, 0]])

    @classmethod
    def _from_rotations(cls, timestamp: np.ndarray, rotations: scipy.spatial.transform.Rotation) -> Self:
        return cls(np.column_stack((timestamp, rotations.as_quat()[:, [3, 0, 1, 2]])))

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 5]))


@dataclass(frozen=True)
class RotationMatrix(OrientationMessage):
    _file_name = "RotationMatrix.csv"

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

    def _to_rotations(self) -> scipy.spatial.transform.Rotation:
        return scipy.spatial.transform.Rotation.from_matrix(self.xx_to_zz.reshape(-1, 3, 3))

    @classmethod
    def _from_rotations(cls, timestamp: np.ndarray, rotations: scipy.spatial.transform.Rotation) -> Self:
        return cls(np.column_stack((timestamp, rotations.as_matrix().reshape(-1, 9))))

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 10]))


@dataclass(frozen=True)
class EulerAngles(OrientationMessage):
    _file_name = "EulerAngles.csv"

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

    def _to_rotations(self) -> scipy.spatial.transform.Rotation:
        return scipy.spatial.transform.Rotation.from_euler("ZYX", self.roll_pitch_yaw[:, [2, 1, 0]], degrees=True)

    @classmethod
    def _from_rotations(cls, timestamp: np.ndarray, rotations: scipy.spatial.transform.Rotation) -> Self:
        return cls(np.column_stack((timestamp, rotations.as_euler("ZYX", degrees=True)[:, [2, 1, 0]])))

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 4]))


@dataclass(frozen=True)
class LinearAcceleration(FloatMessage):
    _file_name = "LinearAcceleration.csv"

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
    _file_name = "EarthAcceleration.csv"

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
    _file_name = "AhrsStatus.csv"


@dataclass(frozen=True)
class SerialAccessory(CharArrayMessage):
    _file_name = "SerialAccessory.csv"


@dataclass(frozen=True)
class Sync(FloatMessage):
    _file_name = "Sync.csv"

    @property
    def edge(self) -> np.ndarray:
        return self._csv[:, 1]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 2]))


@dataclass(frozen=True)
class Ltc(CharArrayMessage):
    _file_name = "Ltc.csv"


@dataclass(frozen=True)
class Temperature(FloatMessage):
    _file_name = "Temperature.csv"

    @property
    def temperature(self) -> np.ndarray:
        return self._csv[:, 1]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 2]))


@dataclass(frozen=True)
class Battery(FloatMessage):
    _file_name = "Battery.csv"

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
    _file_name = "Rssi.csv"

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
    _file_name = "Button.csv"

    @property
    def state(self) -> np.ndarray:
        return self._csv[:, 1]

    @classmethod
    def _empty(cls) -> Self:
        return cls(np.empty([0, 2]))


@dataclass(frozen=True)
class Notification(CharArrayMessage):
    _file_name = "Notification.csv"


@dataclass(frozen=True)
class Error(CharArrayMessage):
    _file_name = "Error.csv"
