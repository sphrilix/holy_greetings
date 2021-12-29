from play_options import PlayOption


class MP3Greet:

    def __init__(self, file_path: str, option: PlayOption = PlayOption.ONLY):
        self.file_path = file_path
        self.option = option

    def __eq__(self, other) -> bool:
        return isinstance(other, MP3Greet) and self.file_path == other.file_path

    def to_json(self) -> dict:
        return {"file_path": self.file_path, "option": self.option.value}

    def __str__(self) -> str:
        return str(self.to_json())
