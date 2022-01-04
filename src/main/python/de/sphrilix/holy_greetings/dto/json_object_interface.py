from abc import ABC, abstractmethod


class JsonObjectInterface(ABC):

    @abstractmethod
    def to_json(self) -> dict:
        pass
