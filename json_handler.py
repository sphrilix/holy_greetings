import json
from user import User


FILE = "./greets.json"


def read() -> list[User]:
    """
    Reads all saved users.
    :return: Returns a list of users. If it is empty returns an empty list.
    """
    users = list()
    with open(FILE, "r") as f:
        data = json.load(f)
        for u_raw in data["users"]:
            users.append(User(u_raw["u_id"], [msg for msg in u_raw["msgs"]]))
    return users


def read_user_by_id(u_id: str) -> User:
    """
    Searches in the saved users for given user id.
    :param u_id: The given user id
    :return: Returns a user if saved, else None.
    """
    users = read()
    for u in users:
        if u_id == u.u_id:
            return u
    return None


def write(user: User) -> None:
    """
    Writes a given user to the storage.
    :param user: The given user.
    """
    users = read()
    if user in users:
        users.remove(user)
    users.append(user)
    with open(FILE, "w") as f:
        data = {"users": [u.to_json() for u in users]}
        json.dump(data, f)

