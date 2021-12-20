import random

from discord import Member, VoiceState, TextChannel
from discord.ext.commands import Bot, Context
import discord
from gtts import gTTS

from json_handler import read_user_by_id, write
from user import User


class HolyGreetingsBot(Bot):
    """

    """

    def __init__(self, token: str, command_prefix: str = "!"):
        """
        Constructor to generate new instance of the HolyGreetingsBot. You can change the command prefix (standard: '!').
        :param command_prefix: Optional if you want to change the prefix.
        """
        super().__init__(command_prefix=command_prefix)

        self.token = token

        @self.command(name="info")
        async def _info(ctx: Context, u_id: str = "unknown") -> None:
            """
            Send an info message about saved greetings for given u_id. If not given just
            :param ctx:
            :param u_id:
            :return:
            """
            await HolyGreetingsBot._info_greet(u_id, ctx.channel)

        @self.command(name="add")
        async def _add(ctx: Context, new_msg: str, u_id: str = "unknown") -> None:
            """

            :param ctx:
            :param new_msg:
            :param u_id:
            :return:
            """
            await HolyGreetingsBot._add_greet(new_msg, u_id)

        @self.command(name="drop")
        async def _drop(ctx: Context, msg: str, u_id: str = "unknown") -> None:
            await HolyGreetingsBot._drop_greet(msg, u_id)

        @self.event
        async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState) -> None:
            if member.id == self.user.id:
                return
            if before.channel is None and after.channel is not None:
                await self._greet(member, after)

    def run(self):
        super().run(self.token)

    async def on_ready(self) -> None:
        print(f"Connected with {self.user.display_name}")

    @staticmethod
    async def _greet(member: Member, after: VoiceState) -> None:
        channel = after.channel
        user = read_user_by_id(member.name)
        msg = random.choice(user.msgs)
        tts = gTTS(msg)
        tts.save("tts.mp3")
        await HolyGreetingsBot._play(channel)

    @staticmethod
    async def _play(channel, track: str = "./tts.mp3") -> None:
        voice_client = await channel.connect(reconnect=False)
        audio_source = await discord.FFmpegOpusAudio.from_probe(track)
        voice_client.play(audio_source)
        while voice_client.is_playing():
            continue
        await voice_client.disconnect()

    @staticmethod
    async def _add_greet(new_msg: str, u_id: str) -> None:
        user = read_user_by_id(u_id)
        if user is None:
            user = User(u_id, list())
        if new_msg not in user.msgs:
            user.msgs.append(new_msg)
        write(user)

    @staticmethod
    async def _drop_greet(msg: str, u_id: str) -> None:
        user = read_user_by_id(u_id)
        if user is None or msg not in user.msgs:
            return
        user.msgs.remove(msg)
        write(user)

    @staticmethod
    async def _info_greet(u_id: str, channel: TextChannel) -> None:
        user = read_user_by_id(u_id)
        if user is None or user.msgs is None or user.msgs == list():
            await HolyGreetingsBot._write_to_channel(f"No greetings found for {u_id}!", channel)
        else:
            await HolyGreetingsBot._write_to_channel(f"For '{u_id}' the following greetings have been found: {chr(10)}"
                                                     + f"{chr(10).join('- ' + msg for msg in user.msgs)}", channel)

    @staticmethod
    async def _write_to_channel(msg: str, channel: TextChannel) -> None:
        await channel.send(msg)
