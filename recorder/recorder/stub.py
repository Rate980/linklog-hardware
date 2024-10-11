from . import gpio, writer


class Stub(gpio.ConnectSense, writer.Writer):
    def __init__(self):
        self._is_connect = True

    def is_connect(self):
        return self._is_connect

    def write(self, data: bytes):
        with open("audio_data", "wb") as f:
            f.write(data)

    def close(self):
        pass
