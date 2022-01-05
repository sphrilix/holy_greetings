import json
import os.path

from de.sphrilix.holy_greetings.dto.greet import Greet
from de.sphrilix.holy_greetings.dto.mp3_greet import MP3Greet
from de.sphrilix.holy_greetings.dto.play_options import to_play_option
from de.sphrilix.holy_greetings.dto.user import User
from de.sphrilix.holy_greetings.persistence.json_handler_interface import JsonHandlerInterface


class GreetingsHandler(JsonHandlerInterface[User]):
    _instance = None

    FILE = "../../../../../../greets.json"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GreetingsHandler, cls).__new__(cls)
        return cls._instance

    def read(self) -> list[User]:
        """
        Reads all saved users.
        :return: Returns a list of users. If it is empty returns an empty list.
        """
        users = list()
        if os.path.getsize(FILE) < 2:
            return users
        with open(self.FILE, "r") as f:
            data = json.load(f)
            for u_raw in data["users"]:
                users.append(self._decode_user(u_raw))
        return users

    def read_user_by_id(self, u_id: str) -> User:
        """
        Searches in the saved users for given user id.
        :param u_id: The given user id
        :return: Returns a user if saved, else None.
        """
        users = self.read()
        for u in users:
            if u_id == u.u_id:
                return u

    def write(self, user: User) -> None:
        """
        Writes a given user to the storage.
        :param user: The given user.
        """
        users = self.read()
        if user in users:
            users.remove(user)
        users.append(user)
        with open(FILE, "w") as f:
            data = {"users": [u.to_json() for u in users]}
            json.dump(data, f)

    @staticmethod
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
