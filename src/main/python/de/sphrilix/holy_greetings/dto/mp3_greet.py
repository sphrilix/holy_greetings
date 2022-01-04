from de.sphrilix.holy_greetings.dto.json_object_interface import JsonObjectInterface
from de.sphrilix.holy_greetings.dto.play_options import PlayOption


class MP3Greet(JsonObjectInterface):

    def __init__(self, file_path: str, option: PlayOption = PlayOption.ONLY):
        self.file_path = file_path
        self.option = option

    def __eq__(self, other) -> bool:
        return isinstance(other, MP3Greet) and self.file_path == other.file_path

    def to_json(self) -> dict:
        return {"file_path": self.file_path, "option": self.option.value}

    def __str__(self) -> str:
        return str(self.to_json())
