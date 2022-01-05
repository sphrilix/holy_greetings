import sys


import os

from de.sphrilix.holy_greetings.dto.config import Config
from de.sphrilix.holy_greetings.persistence.config_handler import ConfigHandler
from de.sphrilix.holy_greetings.web_app import dispatch


sys.path.append("de/sphrilix/holy_greetings")

if __name__ == "__main__":
    if not os.path.exists("../../../../../../mp3/"):
        os.mkdir("../../../../../../mp3/")
    if not ConfigHandler().read():
        c = Config("", 500, 5, 10, 2, 2000000)
        ConfigHandler().write(c)
    try:
        dispatch.APP.run(host="0.0.0.0", port=8080)
        dispatch.BOT_SERVICE.run()
    except KeyboardInterrupt:
        dispatch.BOT_SERVICE.stop()
