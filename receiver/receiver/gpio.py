import abc


class ConnectSense(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_connect(self) -> bool:
        raise NotImplementedError
