import abc
import time
from abc import abstractmethod

import sliplib
from serial import Serial


class Writer(metaclass=abc.ABCMeta):
    @abstractmethod
    def write(self, data: bytes) -> None:
        raise NotImplementedError


class SerialWriter(Writer):
    def __init__(self, port, baudrate) -> None:
        self.serial = Serial(port, baudrate)

    def write(self, data: bytes) -> None:
        time.sleep(0.001)
        num = self.serial.write(sliplib.encode(data))
        if num != len(data):
            raise Exception("Failed to write data")
