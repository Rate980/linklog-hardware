import wave

from .encoder import Mp3EncoderStream
from .gpio import PigpioSense
from .stream import StreamReader
from .stub import Stub
from .writer import SerialWriter


def main():
    main4()


def main1():
    a = Mp3EncoderStream()

    with wave.open("test.wav", "rb") as wf:
        while wf.tell() < 1024 * 300:
            data = wf.readframes(1024)
            a.write(data)

    print("encode")
    res = a.encode()

    with open("test.mp3", "wb") as f:
        f.write(res)


def main2():
    connect_sensor = Stub()
    writer = SerialWriter("/dev/pts/9", 115200)

    connect_sensor._is_connect = True
    streamReader = StreamReader(connect_sensor, writer)
    connect_sensor._is_connect = False

    with wave.open("test.wav", "rb") as wf:
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
    writer = SerialWriter("/dev/pts/9", 115200)
    with open("testdatas/testdata.bin", "rb") as f:
        writer.write(f.read())
