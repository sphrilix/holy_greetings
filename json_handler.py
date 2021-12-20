import json
from user import User


FILE = "./greets.json"


def read() -> list[User]:
    users = list()
    with open(FILE, "r") as f:
        data = json.load(f)
        for u_raw in data["users"]:
            users.append(User(u_raw["u_id"], [msg for msg in u_raw["msgs"]]))
    return users


def read_user_by_id(u_id: str) -> User:
    users = read()
    for u in users:
        if u_id == u.u_id:
            return u
    return None


def write(user: User) -> None:
    users = read()
    if user in users:
        users.remove(user)
    users.append(user)
    with open(FILE, "w") as f:
        data = {"users": [u.to_json() for u in users]}
        json.dump(data, f)

