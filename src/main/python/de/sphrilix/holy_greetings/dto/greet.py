from de.sphrilix.holy_greetings.dto.mp3_greet import MP3Greet


class Greet:

    def __init__(self, msg: str, lang: str = "en", file: MP3Greet = None):
        self.msg = msg
        self.lang = lang
        self.file = file

    def __eq__(self, other):
        return self.msg == other.msg

    def __str__(self):
        return str(self.to_json())

    def to_json(self) -> dict:
        if self.file is None:
            return {"msg": self.msg, "lang": self.lang}
        return {"msg": self.msg, "lang": self.lang, "file": self.file.to_json()}
