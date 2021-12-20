class User:
    def __init__(self, u_id: str, msgs: list[str]):
        self.u_id = u_id
        self.msgs = msgs

    def __str__(self) -> str:
        return str(self.to_json())

    def __eq__(self, other) -> bool:
        return isinstance(other, User) and self.u_id == other.u_id

    def to_json(self) -> dict:
        return {"u_id": self.u_id, "msgs": self.msgs}
