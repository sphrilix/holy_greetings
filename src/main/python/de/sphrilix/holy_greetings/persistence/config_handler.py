import json
import os

from de.sphrilix.holy_greetings.dto.config import Config
from de.sphrilix.holy_greetings.persistence.json_handler_interface import JsonHandlerInterface


class ConfigHandler(JsonHandlerInterface[Config]):

    _instance = None

    CONFIG_FILE = "../../../../../../config.json"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ConfigHandler, cls).__new__(cls)
        return cls._instance

    def read(self) -> Config:
        if not os.path.exists(self.CONFIG_FILE):
            return None
        if os.path.getsize(self.CONFIG_FILE) < 2:
            return None
        with open(self.CONFIG_FILE, "r") as f:
            data = json.load(f)
            return Config(data["token"], data["max_char"], data["max_play"], data["max_play_only"])

    def write(self, config: Config):
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config.to_json(), f)
