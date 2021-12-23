class Greet:

    def __init__(self, msg: str, lang: str = "en"):
        self.msg = msg
        self.lang = lang

    def __eq__(self, other):
        return self.msg == other.msg

    def __str__(self):
        return str(self.to_json())

    def to_json(self) -> dict:
        return {"msg": self.msg, "lang": self.lang}
