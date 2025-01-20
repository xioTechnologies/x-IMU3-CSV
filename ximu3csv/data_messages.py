from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

import numpy as np


class DataMessageType(Enum):
    INERTIAL = auto()
    MAGNETOMETER = auto()
    QUATERNION = auto()
    ROTATION_MATRIX = auto()
    EULER_ANGLES = auto()
    LINEAR_ACCELERATION = auto()
    EARTH_ACCELERATION = auto()
    AHRS_STATUS = auto()
    HIGH_G_ACCELEROMETER = auto()
    TEMPERATURE = auto()
    BATTERY = auto()
    RSSI = auto()
    SERIAL_ACCESSORY = auto()
    NOTIFICATION = auto()
    ERROR = auto()

    @property
    def file_name(self) -> str:
        match self:
            case DataMessageType.INERTIAL:
                base_name = "Inertial"
            case DataMessageType.MAGNETOMETER:
                base_name = "Magnetometer"
            case DataMessageType.QUATERNION:
                base_name = "Quaternion"
            case DataMessageType.ROTATION_MATRIX:
                base_name = "RotationMatrix"
            case DataMessageType.EULER_ANGLES:
                base_name = "EulerAngles"
            case DataMessageType.LINEAR_ACCELERATION:
                base_name = "LinearAcceleration"
            case DataMessageType.EARTH_ACCELERATION:
                base_name = "EarthAcceleration"
            case DataMessageType.AHRS_STATUS:
                base_name = "AhrsStatus"
            case DataMessageType.HIGH_G_ACCELEROMETER:
                base_name = "HighGAccelerometer"
            case DataMessageType.TEMPERATURE:
                base_name = "Temperature"
            case DataMessageType.BATTERY:
                base_name = "Battery"
            case DataMessageType.RSSI:
                base_name = "Rssi"
            case DataMessageType.SERIAL_ACCESSORY:
                base_name = "SerialAccessory"
            case DataMessageType.NOTIFICATION:
                base_name = "Notification"
            case DataMessageType.ERROR:
                base_name = "Error"

        return f"{base_name}.csv"


@dataclass(frozen=True)
class __DataMessage(ABC):
    _csv: np.ndarray
    _string: str

    @property
    def timestamp(self) -> np.ndarray:
        return self._csv[:, 0]


@dataclass(frozen=True)
class Xyz:
    __csv: np.ndarray
    __column: int

    @property
    def xyz(self) -> np.ndarray:
        return self.__csv[:, self.__column : self.__column + 3]

    @property
    def x(self) -> np.ndarray:
        return self.__csv[:, self.__column]

    @property
    def y(self) -> np.ndarray:
        return self.__csv[:, self.__column + 1]

    @property
    def z(self) -> np.ndarray:
        return self.__csv[:, self.__column + 2]


@dataclass(frozen=True)
class Wxyz:
    __csv: np.ndarray
    __column: int

    @property
    def wxyz(self) -> np.ndarray:
        return self.__csv[:, self.__column : self.__column + 4]

    @property
    def w(self) -> np.ndarray:
        return self.__csv[:, self.__column]

    @property
    def x(self) -> np.ndarray:
        return self.__csv[:, self.__column + 1]

    @property
    def y(self) -> np.ndarray:
        return self.__csv[:, self.__column + 2]

    @property
    def z(self) -> np.ndarray:
        return self.__csv[:, self.__column + 3]


@dataclass(frozen=True)
class Inertial(__DataMessage):
    @property
    def gyroscope(self) -> Xyz:
        return Xyz(self._csv, 1)

    @property
    def accelerometer(self) -> Xyz:
        return Xyz(self._csv, 4)


@dataclass(frozen=True)
class Magnetometer(__DataMessage):
    @property
    def magnetometer(self) -> Xyz:
        return Xyz(self._csv, 1)


@dataclass(frozen=True)
class Quaternion(__DataMessage):
    @property
    def quaternion(self) -> Wxyz:
        return Wxyz(self._csv, 1)


@dataclass(frozen=True)
class RotationMatrix(__DataMessage):
    @property
    def rotation_matrix(self) -> np.ndarray:
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


@dataclass(frozen=True)
class EulerAngles(__DataMessage):
    @property
    def euler_angles(self) -> np.ndarray:
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


@dataclass(frozen=True)
class LinearAcceleration(__DataMessage):
    @property
    def quaternion(self) -> Wxyz:
        return Wxyz(self._csv, 1)

    @property
    def linear_acceleration(self) -> Xyz:
        return Xyz(self._csv, 5)


@dataclass(frozen=True)
class EarthAcceleration(__DataMessage):
    @property
    def quaternion(self) -> Wxyz:
        return Wxyz(self._csv, 1)

    @property
    def earth_acceleration(self) -> Xyz:
        return Xyz(self._csv, 5)


@dataclass(frozen=True)
class AhrsStatus(__DataMessage):
    @property
    def initialising(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def angular_rate_recovery(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def acceleration_rate_recovery(self) -> np.ndarray:
        return self._csv[:, 3]

    @property
    def magnetic_rate_recovery(self) -> np.ndarray:
        return self._csv[:, 4]


@dataclass(frozen=True)
class HighGAccelerometer(__DataMessage):
    @property
    def high_g_accelerometer(self) -> Xyz:
        return Xyz(self._csv, 1)


@dataclass(frozen=True)
class Temperature(__DataMessage):
    @property
    def temperature(self) -> np.ndarray:
        return self._csv[:, 1]


@dataclass(frozen=True)
class Battery(__DataMessage):
    @property
    def percentage(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def voltage(self) -> np.ndarray:
        return self._csv[:, 2]

    @property
    def charging_status(self) -> np.ndarray:
        return self._csv[:, 3]


@dataclass(frozen=True)
class Rssi(__DataMessage):
    @property
    def percentage(self) -> np.ndarray:
        return self._csv[:, 1]

    @property
    def power(self) -> np.ndarray:
        return self._csv[:, 2]


@dataclass(frozen=True)
class SerialAccessory(__DataMessage):
    @property
    def csv(self) -> np.ndarray:
        return self._csv[:, 1:]


@dataclass(frozen=True)
class Notification(__DataMessage):
    @property
    def string(self) -> List[str]:
        return self._string


@dataclass(frozen=True)
class Error(__DataMessage):
    @property
    def string(self) -> List[str]:
        return self._string
