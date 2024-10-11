from collections import deque

import serial
import sliplib


class Uart:
    def __init__(self, port: serial.Serial):
        self.port = port
        self.slip_driver = sliplib.Driver()
        self.dataQueue: deque[bytes] = deque()

    def read(self):
        data = self.port.read_all()
        if data is None:
            return

        self.dataQueue.extend(self.slip_driver.receive(data))

    def write(self, data):
        self.port.write(self.slip_driver.send(data))

    def pop(self):
        if len(self.dataQueue) == 0:
            return None
        return self.dataQueue.popleft()


if __name__ == "__main__":
    port = serial.Serial("/dev/pts/6", 115200)
    uart = Uart(port)
    i = 0
    while True:
        uart.read()
        data = uart.pop()
        if data is not None:
            with open(f"output{i}", "wb") as f:
                f.write(data)
                i += 1
