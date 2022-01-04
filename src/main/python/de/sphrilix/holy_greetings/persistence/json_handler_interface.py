from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class JsonHandlerInterface(ABC, Generic[T]):

    @abstractmethod
    def read(self) -> T:
        pass

    @abstractmethod
    def write(self, t: T) -> None:
        pass
