import json
import numpy
import os
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto


class MessageType(Enum):
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
    def file_name(self):
        match self:
            case MessageType.INERTIAL:
                base_name = "Inertial"
            case MessageType.MAGNETOMETER:
                base_name = "Magnetometer"
            case MessageType.QUATERNION:
                base_name = "Quaternion"
            case MessageType.ROTATION_MATRIX:
                base_name = "RotationMatrix"
            case MessageType.EULER_ANGLES:
                base_name = "EulerAngles"
            case MessageType.LINEAR_ACCELERATION:
                base_name = "LinearAcceleration"
            case MessageType.EARTH_ACCELERATION:
                base_name = "EarthAcceleration"
            case MessageType.AHRS_STATUS:
                base_name = "AhrsStatus"
            case MessageType.HIGH_G_ACCELEROMETER:
                base_name = "HighGAccelerometer"
            case MessageType.TEMPERATURE:
                base_name = "Temperature"
            case MessageType.BATTERY:
                base_name = "Battery"
            case MessageType.RSSI:
                base_name = "Rssi"
            case MessageType.SERIAL_ACCESSORY:
                base_name = "SerialAccessory"
            case MessageType.NOTIFICATION:
                base_name = "Notification"
            case MessageType.ERROR:
                base_name = "Error"

        return base_name + ".csv"


class __Message(ABC):
    @abstractmethod
    def __init__(self, directory, message_types, message_type):
        self._numerical = numpy.empty([0, 10])  # 10 is the maximum number of columns expected of any message type
        self._string = numpy.empty([0, 1])

        if message_type not in message_types:
            return

        file_path = os.path.join(directory, message_type.file_name)

        if not os.path.isfile(file_path):
            return

        self._numerical = numpy.genfromtxt(file_path, delimiter=",", skip_header=1)

        if message_type in (MessageType.NOTIFICATION, MessageType.ERROR):
            self._string = numpy.genfromtxt(file_path, delimiter=",", skip_header=1, usecols=1, dtype=None, encoding=None)  # TODO: Handle strings that contain commas

    @property
    def timestamp(self):
        return self._numerical[:, 0]


class Xyz():
    def __init__(self, data, column):
        self._numerical = data[:, column:(column + 3)]

    @property
    def xyz(self):
        return self._numerical[:, :]

    @property
    def x(self):
        return self._numerical[:, 0]

    @property
    def y(self):
        return self._numerical[:, 1]

    @property
    def z(self):
        return self._numerical[:, 2]


class Wxyz():
    def __init__(self, data, column):
        self._numerical = data[:, column:(column + 4)]

    @property
    def wxyz(self):
        return self._numerical[:, :]

    @property
    def w(self):
        return self._numerical[:, 0]

    @property
    def x(self):
        return self._numerical[:, 1]

    @property
    def y(self):
        return self._numerical[:, 2]

    @property
    def z(self):
        return self._numerical[:, 3]


class Inertial(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.INERTIAL)

    @property
    def gyroscope(self):
        return Xyz(self._numerical, 1)

    @property
    def accelerometer(self):
        return Xyz(self._numerical, 4)


class Magnetometer(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.MAGNETOMETER)

    @property
    def magnetometer(self):
        return Xyz(self._numerical, 1)


class Quaternion(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.QUATERNION)

    @property
    def quaternion(self):
        return Wxyz(self._numerical, 1)


class RotationMatrix(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.ROTATION_MATRIX)

    @property
    def rotation_matrix(self):
        return self._numerical[:, 1:10]

    @property
    def xx(self):
        return self._numerical[:, 1]

    @property
    def xy(self):
        return self._numerical[:, 2]

    @property
    def xz(self):
        return self._numerical[:, 3]

    @property
    def yx(self):
        return self._numerical[:, 4]

    @property
    def yy(self):
        return self._numerical[:, 5]

    @property
    def yz(self):
        return self._numerical[:, 6]

    @property
    def zx(self):
        return self._numerical[:, 7]

    @property
    def zy(self):
        return self._numerical[:, 8]

    @property
    def zz(self):
        return self._numerical[:, 9]


class EulerAngles(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.EULER_ANGLES)

    @property
    def euler_angles(self):
        return self._numerical[:, 1:4]

    @property
    def roll(self):
        return self._numerical[:, 1]

    @property
    def pitch(self):
        return self._numerical[:, 2]

    @property
    def yaw(self):
        return self._numerical[:, 3]


class LinearAcceleration(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.LINEAR_ACCELERATION)

    @property
    def quaternion(self):
        return Wxyz(self._numerical, 1)

    @property
    def linear_acceleration(self):
        return Xyz(self._numerical, 5)


class EarthAcceleration(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.EARTH_ACCELERATION)

    @property
    def quaternion(self):
        return Wxyz(self._numerical, 1)

    @property
    def earth_acceleration(self):
        return Xyz(self._numerical, 5)


class AhrsStatus(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.AHRS_STATUS)

    @property
    def initialising(self):
        return self._numerical[:, 1]

    @property
    def angular_rate_recovery(self):
        return self._numerical[:, 2]

    @property
    def acceleration_rate_recovery(self):
        return self._numerical[:, 3]

    @property
    def magnetic_rate_recovery(self):
        return self._numerical[:, 4]


class HighGAccelerometer(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.HIGH_G_ACCELEROMETER)

    @property
    def high_g_accelerometer(self):
        return Xyz(self._numerical, 1)


class Temperature(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.TEMPERATURE)

    @property
    def temperature(self):
        return self._numerical[:, 1]


class Battery(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.BATTERY)

    @property
    def percentage(self):
        return self._numerical[:, 1]

    @property
    def voltage(self):
        return self._numerical[:, 2]

    @property
    def charging_status(self):
        return self._numerical[:, 3]


class Rssi(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.RSSI)

    @property
    def percentage(self):
        return self._numerical[:, 1]

    @property
    def power(self):
        return self._numerical[:, 2]


class SerialAccessory(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.SERIAL_ACCESSORY)

    @property
    def csv(self):
        return self._numerical[:, 1:]


class Notification(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.NOTIFICATION)

    @property
    def string(self):
        return self._string


class Error(__Message):
    def __init__(self, directory, message_types):
        super().__init__(directory, message_types, MessageType.ERROR)

    @property
    def string(self):
        return self._string


class Device():
    def __init__(self, directory, message_types):
        file_path = os.path.join(directory, "Command.json")

        if os.path.isfile(file_path):
            with open(file_path) as file:
                self.__command = json.load(file)
        else:
            self.__command = []

        self.__interface, self.__device_name, self.__serial_number = Device.__get_ping(self.command)

        self.__time = Device.__get_time(self.command)

        self.__inertial = Inertial(directory, message_types)

        self.__magnetometer = Magnetometer(directory, message_types)

        self.__quaternion = Quaternion(directory, message_types)

        self.__rotation_matrix = RotationMatrix(directory, message_types)

        self.__euler_angles = EulerAngles(directory, message_types)

        self.__linear_acceleration = LinearAcceleration(directory, message_types)

        self.__earth_acceleration = EarthAcceleration(directory, message_types)

        self.__ahrs_status = AhrsStatus(directory, message_types)

        self.__high_g_accelerometer = HighGAccelerometer(directory, message_types)

        self.__temperature = Temperature(directory, message_types)

        self.__battery = Battery(directory, message_types)

        self.__rssi = Rssi(directory, message_types)

        self.__serial_accessory = SerialAccessory(directory, message_types)

        self.__notification = Notification(directory, message_types)

        self.__error = Error(directory, message_types)

    @staticmethod
    def __get_ping(commands):
        for command in commands:
            for key, value in command.items():
                if key == "ping":
                    return value["interface"], value["deviceName"],  value["serialNumber"]

        return None, None, None

    @staticmethod
    def __get_time(commands):
        for command in commands:
            for key, value in command.items():
                if key == "time":
                    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

        return None

    @property
    def command(self):
        return self.__command

    @property
    def interface(self):
        return self.__interface

    @property
    def device_name(self):
        return self.__device_name

    @property
    def serial_number(self):
        return self.__serial_number

    @property
    def time(self):
        return self.__time

    @property
    def inertial(self):
        return self.__inertial

    @property
    def magnetometer(self):
        return self.__magnetometer

    @property
    def quaternion(self):
        return self.__quaternion

    @property
    def rotation_matrix(self):
        return self.__rotation_matrix

    @property
    def euler_angles(self):
        return self.__euler_angles

    @property
    def linear_acceleration(self):
        return self.__linear_acceleration

    @property
    def earth_acceleration(self):
        return self.__earth_acceleration

    @property
    def ahrs_status(self):
        return self.__ahrs_status

    @property
    def high_g_accelerometer(self):
        return self.__high_g_accelerometer

    @property
    def temperature(self):
        return self.__temperature

    @property
    def battery(self):
        return self.__battery

    @property
    def rssi(self):
        return self.__rssi

    @property
    def serial_accessory(self):
        return self.__serial_accessory

    @property
    def notification(self):
        return self.__notification

    @property
    def error(self):
        return self.__error


def read(root, message_types=MessageType):
    if not os.path.isdir(root):
        raise Exception("\"" + root + "\" does not exist")

    directories = [os.path.join(root, d) for d in os.listdir(root) if not d.startswith('.')]

    if not directories:
        raise Exception("\"" + root + "\" is empty")

    return [Device(d, message_types) for d in directories]
