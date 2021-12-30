import json
import os.path

from de.sphrilix.holy_greetings.dto.greet import Greet
from de.sphrilix.holy_greetings.dto.mp3_greet import MP3Greet
from de.sphrilix.holy_greetings.dto.play_options import to_play_option
from de.sphrilix.holy_greetings.dto.user import User

FILE = "../../../../../../greets.json"


def read() -> list[User]:
    """
    Reads all saved users.
    :return: Returns a list of users. If it is empty returns an empty list.
    """
    users = list()
    if os.path.getsize(FILE) < 2:
        return users
    with open(FILE, "r") as f:
        data = json.load(f)
        for u_raw in data["users"]:
            users.append(_decode_user(u_raw))
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


def _decode_user(u_raw: json) -> User:
    u_id = u_raw["u_id"]
    raw_msgs = u_raw["msgs"]
    msgs: list[Greet] = list()
    for raw_msg in raw_msgs:
        if "file" in raw_msg:
            raw_file = raw_msg["file"]
            msgs.append(Greet(raw_msg["msg"], raw_msg["lang"], MP3Greet(raw_file["file_path"],
                                                                        to_play_option(raw_file["option"]))))
        else:
            msgs.append(Greet(raw_msg["msg"], raw_msg["lang"]))
    return User(u_id, msgs)
