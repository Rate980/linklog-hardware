import abc
from abc import abstractmethod

import pyaudio

from receiver import encoder

from .gpio import ConnectSense
from .writer import Writer


class PyaudoStreamReader(metaclass=abc.ABCMeta):
    @abstractmethod
    def callback(
        self, in_data, frame_count, time_info, status
    ) -> tuple[bytes | None, int]:
        raise NotImplementedError


class MicStream:
    def __init__(
        self,
        streamReader: PyaudoStreamReader,
        chunk_size=1024,
        sample_rate=44100,
        channels=1,
        format=pyaudio.paInt16,
    ) -> None:
        self.audio = pyaudio.PyAudio()
        self.streamReader = streamReader
        self.stream = self.stream.open(
            format=format,
            channels=channels,
            rate=sample_rate,
            input=True,
            output=False,
            frames_per_buffer=chunk_size,
            stream_callback=streamReader.callback,
        )

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


class StreamReader(PyaudoStreamReader):
    def __init__(
        self,
        coenact_sense: ConnectSense,
        writer: Writer,
    ):
        self.coenact_sense = coenact_sense
        self.writer = writer
        self.is_connected = coenact_sense.is_connect()
        self.audio_data = bytearray()

    def callback(self, in_data, frame_count, time_info, status):
        is_connect = self.coenact_sense.is_connect()
        is_connected = self.is_connected
        self.is_connected = is_connect
        self.callback_input(
            in_data, frame_count, time_info, status, is_connect, is_connected
        )
        return None, pyaudio.paContinue

    def callback_input(
        self, in_data, frame_count, time_info, status, is_connect, is_connected
    ) -> None:
        if is_connect:
            if not is_connected:
                print("Connect")
                self.writer.write(encoder.encode(self.audio_data))

        else:
            if is_connected:
                print("Disconnect")
                self.audio_data.clear()

            self.audio_data.extend(in_data)
