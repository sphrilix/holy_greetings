from de.sphrilix.holy_greetings.dto.json_object_interface import JsonObjectInterface


class Config(JsonObjectInterface):
    def __init__(self, token: str, max_char: int, max_play: int, max_play_only: int):
        self.token = token
        self.max_char = max_char
        self.max_play = max_play
        self.max_play_only = max_play_only

    def to_json(self) -> dict:
        return {"token": self.token,
                "max_char": self.max_char,
                "max_play": self.max_play,
                "max_play_only": self.max_play_only}
