from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class JsonHandlerInterface(ABC, Generic[T]):
    """
    Interface for classes who are reading and writing objects to the hard rive.
    """

    @abstractmethod
    def read(self) -> T:
        """
        Read from file.
        :return: Returns read object.
        """
        pass

    @abstractmethod
    def write(self, t: T) -> None:
        """
        Write to file.
        :param t: Object to be written to the file.
        """
        pass
