import json
import numpy
import os
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto


class MessageType(Enum):
    INTERTIAL = auto()
    MAGNETOMETER = auto()
    QUATERNION = auto()
    ROTATION_MATRIX = auto()
    EULER = auto()
    LINEAR_ACCELERATION = auto()
    EARTH_ACCELERATION = auto()
    HIGH_G_ACCELEROMETER = auto()
    TEMPERATURE = auto()
    BATTERY = auto()
    RSSI = auto()
    SERIAL_ACCESSORY = auto()
    NOTIFCATION = auto()
    ERROR = auto()


class __Message(ABC):
    @abstractmethod
    def __init__(self, directory, name, string=False):
        file_name = os.path.join(directory, name + ".csv")

        try:
            self.data = numpy.genfromtxt(file_name, delimiter=",", skip_header=1)

            if string:
                self._string = numpy.genfromtxt(file_name, delimiter=",", skip_header=1, usecols=1, dtype=None, encoding=None)
        except:
            self.data = None

    @property
    def timestamp(self):
        return self.data[:, 0]


class Xyz():
    def __init__(self, data, index):
        self.data = data[:, index:(index + 3)]

    @property
    def xyz(self):
        return self.data[:, :]

    @property
    def x(self):
        return self.data[:, 0]

    @property
    def y(self):
        return self.data[:, 1]

    @property
    def z(self):
        return self.data[:, 2]


class Wxyz():
    def __init__(self, data, index):
        self.data = data[:, index:(index + 4)]

    @property
    def wxyz(self):
        return self.data[:, :]

    @property
    def w(self):
        return self.data[:, 0]

    @property
    def x(self):
        return self.data[:, 1]

    @property
    def y(self):
        return self.data[:, 2]

    @property
    def z(self):
        return self.data[:, 3]


class Inertial(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Inertial")

    @property
    def gyroscope(self):
        return Xyz(self.data, 1)

    @property
    def accelerometer(self):
        return Xyz(self.data, 4)


class Magnetometer(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Magnetometer")

    @property
    def magnetometer(self):
        return Xyz(self.data, 1)


class Quaternion(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Quaternion")

    @property
    def quaternion(self):
        return Wxyz(self.data, 1)


class RotationMatrix(__Message):
    def __init__(self, directory):
        super().__init__(directory, "RotationMatrix")

    @property
    def xx(self):
        return self.data[:, 1]

    @property
    def xy(self):
        return self.data[:, 2]

    @property
    def xz(self):
        return self.data[:, 3]

    @property
    def yx(self):
        return self.data[:, 4]

    @property
    def yy(self):
        return self.data[:, 5]

    @property
    def yz(self):
        return self.data[:, 6]

    @property
    def zx(self):
        return self.data[:, 7]

    @property
    def zy(self):
        return self.data[:, 8]

    @property
    def zz(self):
        return self.data[:, 9]


class Euler(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Euler")

    @property
    def roll(self):
        return self.data[:, 1]

    @property
    def pitch(self):
        return self.data[:, 2]

    @property
    def yaw(self):
        return self.data[:, 3]


class LinearAcceleration(__Message):
    def __init__(self, directory):
        super().__init__(directory, "LinearAcceleration")

    @property
    def quaternion(self):
        return Wxyz(self.data, 1)

    @property
    def linearAcceleration(self):
        return Xyz(self.data, 5)


class EarthAcceleration(__Message):
    def __init__(self, directory):
        super().__init__(directory, "EarthAcceleration")

    @property
    def quaternion(self):
        return Wxyz(self.data, 1)

    @property
    def earthAcceleration(self):
        return Xyz(self.data, 5)


class HighGAccelerometer(__Message):
    def __init__(self, directory):
        super().__init__(directory, "HighGAccelerometer")

    @property
    def high_g_accelerometer(self):
        return Xyz(self.data, 1)


class Temperature(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Temperature")

    @property
    def temperature(self):
        return self.data[:, 1]


class Battery(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Battery")

    @property
    def percentage(self):
        return self.data[:, 1]

    @property
    def voltage(self):
        return self.data[:, 2]

    @property
    def chargingStatus(self):
        return self.data[:, 3]


class Rssi(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Rssi")

    @property
    def percentage(self):
        return self.data[:, 1]

    @property
    def power(self):
        return self.data[:, 2]


class SerialAccessory(__Message):
    def __init__(self, directory):
        super().__init__(directory, "SerialAccessory")

    @property
    def values(self):
        return self.data[:, 1:]


class Notification(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Notification", True)

    @property
    def string(self):
        return self._string


class Error(__Message):
    def __init__(self, directory):
        super().__init__(directory, "Error", True)

    @property
    def string(self):
        return self._string


class Device():
    def __init__(self, directory, message_types):
        with open(os.path.join(directory, "Command.json")) as json_file:
            self.command = json.load(json_file)

        self.interface, self.device_name, self.serial_number = Device.__get_ping(self.command)

        self.time = Device.__get_time(self.command)

        if not message_types or MessageType.INTERTIAL in message_types:
            self.inertial = Inertial(directory)

        if not message_types or MessageType.MAGNETOMETER in message_types:
            self.magnetometer = Magnetometer(directory)

        if not message_types or MessageType.QUATERNION in message_types:
            self.quaternion = Quaternion(directory)

        if not message_types or MessageType.ROTATION_MATRIX in message_types:
            self.rotation_matrix = RotationMatrix(directory)

        if not message_types or MessageType.EULER in message_types:
            self.euler = Euler(directory)

        if not message_types or MessageType.LINEAR_ACCELERATION in message_types:
            self.linearAcceleration = LinearAcceleration(directory)

        if not message_types or MessageType.EARTH_ACCELERATION in message_types:
            self.earthAcceleration = EarthAcceleration(directory)

        if not message_types or MessageType.HIGH_G_ACCELEROMETER in message_types:
            self.high_g_accelerometer = HighGAccelerometer(directory)

        if not message_types or MessageType.TEMPERATURE in message_types:
            self.temperature = Temperature(directory)

        if not message_types or MessageType.BATTERY in message_types:
            self.battery = Battery(directory)

        if not message_types or MessageType.RSSI in message_types:
            self.rssi = Rssi(directory)

        if not message_types or MessageType.SERIAL_ACCESSORY in message_types:
            self.serial_accessory = SerialAccessory(directory)

        if not message_types or MessageType.NOTIFCATION in message_types:
            self.notification = Notification(directory)

        if not message_types or MessageType.ERROR in message_types:
            self.error = Error(directory)

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
                    try:
                        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    except:
                        return None

        return None

def listdir_ignore_hidden(directory):
    result = []
    for d in os.listdir(directory):
        if not d.startswith('.'):
            result.append(d)
    return result

def import_data(session_directory, message_types=[]):
    return [Device(os.path.join(session_directory, d), message_types) for d in listdir_ignore_hidden(session_directory)]
