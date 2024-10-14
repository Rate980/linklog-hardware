import abc
import time
import wave
from abc import abstractmethod

import sliplib
from serial import Serial


class Writer(metaclass=abc.ABCMeta):
    @abstractmethod
    def write(self, data: bytes) -> None:
        raise NotImplementedError


class SerialWriter(Writer):
    def __init__(self, port: Serial) -> None:
        self.serial = port

    def write(self, data: bytes) -> None:
        time.sleep(0.001)
        data = sliplib.encode(data)
        num = self.serial.write(data)
        if num != len(data):
            raise Exception("Failed to write data")

        self.serial.flush()


class WaveWriter(Writer):
    def write(self, data: bytes) -> None:
        with wave.open("audio_data.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(data)
