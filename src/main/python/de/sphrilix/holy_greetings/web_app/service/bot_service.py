import asyncio
from threading import Thread

from de.sphrilix.holy_greetings.bot.holy_greetings_bot import HolyGreetingsBot
from de.sphrilix.holy_greetings.dto.config import Config
from de.sphrilix.holy_greetings.persistence.config_handler import ConfigHandler


class BotService(Thread):
    _CONFIG_HANDLER = ConfigHandler()

    _BOT_INSTANCE = None

    token = ""

    _loop = None

    def __init__(self):
        Thread.__init__(self)
        self._loop = asyncio.get_event_loop()
        self.start()
        config: Config = self._CONFIG_HANDLER.read()
        if config and config.token != "":
            print("here")
            self.token = config.token

    def run(self) -> None:
        if not self._BOT_INSTANCE and self.token != "":
            c = ConfigHandler().read()
            c.token = self.token
            ConfigHandler().write(c)
            self.name = "bot_service_thread"
            self._loop.create_task(self._run_bot())
            self._loop.run_forever()

    async def _run_bot(self) -> None:
        if not self._BOT_INSTANCE:
            self._BOT_INSTANCE = HolyGreetingsBot(self.token)
        await self._BOT_INSTANCE.start_bot()

    def is_running(self) -> bool:
        return self.token != ""

    def update_config(self, c: Config) -> None:
        print("hello")
        if self._BOT_INSTANCE:
            self._BOT_INSTANCE.max_char = c.max_char
            self._BOT_INSTANCE.max_play = c.max_play
            self._BOT_INSTANCE.max_play_only = c.max_play_only
            self._BOT_INSTANCE.max_sound_size = c.max_sound_size
            self._BOT_INSTANCE.max_sound_greets = c.max_sound_greets
        config = ConfigHandler().read()
        config.max_char = c.max_char
        config.max_play = c.max_play
        config.max_play_only = c.max_play_only
        config.max_sound_greets = c.max_sound_greets
        config.max_sound_size = c.max_sound_size
        ConfigHandler().write(config)

    def stop(self):
        self.join(1)

    @staticmethod
    def get_config():
        return ConfigHandler().read()

