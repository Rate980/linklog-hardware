import abc
import subprocess
from abc import abstractmethod


class Encoder(metaclass=abc.ABCMeta):
    @abstractmethod
    def encode(self, data: bytes) -> bytes:
        raise NotImplementedError


class StreamEncoder(metaclass=abc.ABCMeta):
    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def write(self, bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


def encode(data: bytes) -> bytes:
    cmd = ["lame", "--quiet", "-r", "-s" "44.1", "-m", "m", "-b", "192" "-", "-"]
    process = subprocess.run(cmd, input=data, stdout=subprocess.PIPE)
    return process.stdout


class Mp3Encoder(Encoder):
    def encode(self, data: bytes) -> bytes:
        cmd = ["lame", "--quiet", "-r", "-s" "44.1", "-b", "192", "-", "-"]
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        process.stdin.write(data)  # type: ignore
        process.stdin.close()  # type: ignore
        process.wait()
        return process.stdout.read()  # type: ignore


class Mp3EncoderStream(StreamEncoder):
    def __init__(self):
        self.cmd = ["lame", "--quiet", "-r", "-s" "44.1", "-b", "192", "-", "-"]
        self.process = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def encode(self) -> bytes:
        self.process.stdin.close()  # type: ignore
        self.process.wait()
        return self.process.stdout.read()  # type: ignore

    def write(self, bytes) -> None:
        if self.process.poll() is not None:
            self.process = subprocess.Popen(
                self.cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )

        self.process.stdin.write(bytes)  # type: ignore

    def close(self):
        self.process.kill()
