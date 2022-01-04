from de.sphrilix.holy_greetings.dto.config import Config
from de.sphrilix.holy_greetings.persistence.config_handler import ConfigHandler
from de.sphrilix.holy_greetings.web_app import dispatch

if __name__ == "__main__":
    if not ConfigHandler().read():
        c = Config("", 500, 5, 10)
        ConfigHandler().write(c)
    dispatch.APP.run(debug=True)
