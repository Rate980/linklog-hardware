import abc
from abc import abstractmethod

import pigpio
from pigpio import HIGH


class ConnectSense(metaclass=abc.ABCMeta):
    @abstractmethod
    def is_connect(self) -> bool:
        raise NotImplementedError


class PigpioSense(ConnectSense):
    def __init__(self, pin_num) -> None:
        self.pi = pi = pigpio.pi()
        self.pin_num = pin_num
        pi.set_mode(pin_num, pigpio.INPUT)

        super().__init__()

    def is_connect(self) -> bool:
        return self.pi.read(self.pin_num) == HIGH
