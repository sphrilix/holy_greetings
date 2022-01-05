from abc import ABC, abstractmethod


class JsonObjectInterface(ABC):
    """
    Interface for object to be serialized to JSON
    """

    @abstractmethod
    def to_json(self) -> dict:
        """
        To JSON.
        :return: JSON repr
        """
        pass
