import abc


class Writer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, data: bytes) -> None:
        raise NotImplementedError
