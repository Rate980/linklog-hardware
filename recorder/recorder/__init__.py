import os
import time
import wave

import serial
from dotenv import load_dotenv

from .encoder import Mp3EncoderStream
from .gpio import PigpioSense
from .stream import MicStream, StreamReader
from .stub import Stub
from .writer import SerialWriter

load_dotenv()


def main():
    main5()
    connect_senser = PigpioSense(17)
    port = serial.Serial(os.environ["TTY_PATH"], int(os.environ["BANDRATE"]))
    writer = SerialWriter(port)
    streamReader = StreamReader(connect_senser, writer)
    stream = MicStream(streamReader)
    stream.stream.start_stream()
    while stream.stream.is_active():
        time.sleep(1)


def main1():
    a = Mp3EncoderStream()

    with wave.open("testdatas/test.wav", "rb") as wf:
        while wf.tell() < 1024 * 300:
            data = wf.readframes(1024)
            a.write(data)

    print("encode")
    res = a.encode()

    with open("testdatas/test.mp3", "wb") as f:
        f.write(res)


def main2():
    connect_sensor = Stub()
    port = serial.Serial("/dev/pts/9", 115200)
    writer = SerialWriter(port)

    connect_sensor._is_connect = True
    streamReader = StreamReader(connect_sensor, writer)
    connect_sensor._is_connect = False

    with wave.open("testdatas/test.wav", "rb") as wf:
        while wf.tell() < wf.getnframes():
            data = wf.readframes(1024)
            streamReader.callback(data, 1024, None, None)

    connect_sensor._is_connect = True
    data = b"\x00" * 1024 * 2
    streamReader.callback(data, 1024, None, None)


def main3():
    connect_sensor = PigpioSense(17)
    while True:
        print(connect_sensor.is_connect())


def main4():
    port = serial.Serial("/dev/pts/9", 115200)
    writer = SerialWriter(port)
    with open("testdatas/testdata.bin", "rb") as f:
        writer.write(f.read())


def main5():
    connect_sensor = PigpioSense(17)
    port = serial.Serial(os.environ["TTY_PATH"], int(os.environ["BANDRATE"]))
    writer = SerialWriter(port)
    old_state = connect_sensor.is_connect()
    data = b"\xde\xad\xbe\xef" * 10
    while True:
        state = connect_sensor.is_connect()

        if state and not old_state:
            print("Connect")
            time.sleep(1)
            writer.write(data)

        old_state = state
