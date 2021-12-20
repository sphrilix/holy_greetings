import random

from discord import Member, VoiceState, TextChannel
from discord.ext.commands import Bot, Context
import discord
from gtts import gTTS

from json_handler import read_user_by_id, write
from user import User


class HolyGreetingsBot(Bot):
    """
    The HolyGreetingsBot to manage customizable greetings on your Discord server.
    """

    def __init__(self, token: str, command_prefix: str = "!"):
        """
        Constructor to generate new instance of the HolyGreetingsBot. You can change the command prefix (standard: '!').
        :param command_prefix: Optional if you want to change the prefix.
        :param token: The token needed to identify and register the bot.
        """
        super().__init__(command_prefix=command_prefix)

        self.token = token

        @self.command(name="info")
        async def _info(ctx: Context, u_id: str = "unknown") -> None:
            """
            Send an info message about saved greetings for given u_id. If not given just get info for unknown user.
            :param ctx: Context of the command.
            :param u_id: The given user id.
            """
            await HolyGreetingsBot._info_greet(u_id, ctx.channel)

        @self.command(name="add")
        async def _add(_: Context, new_msg: str, u_id: str = "unknown") -> None:
            """
            Add a new given greeting for the given user id.
            :param _:
            :param new_msg: The given user id.
            :param u_id: The given new greeting
            """
            await HolyGreetingsBot._add_greet(new_msg, u_id)

        @self.command(name="drop")
        async def _drop(_: Context, msg: str, u_id: str = "unknown") -> None:
            """
            Drop a given greeting for the given user id.
            :param _:
            :param new_msg: The given user id.
            :param u_id: The given greeting.
            """
            await HolyGreetingsBot._drop_greet(msg, u_id)

        @self.event
        async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState) -> None:
            """
            Listen on server and check whether someone connected or not. If so greet the joined user with the
            appropriate greeting.
            :param member: Member which state has changed.
            :param before: Status before change.
            :param after: Status after change.
            """
            if member.id == self.user.id:
                return
            if before.channel is None and after.channel is not None:
                await self._greet(member, after)

    def run(self) -> None:
        """
        Start the bot.
        """
        super().run(self.token)

    async def on_ready(self) -> None:
        """
        Print out when ready.
        """
        print(f"Connected with {self.user.display_name}")

    @staticmethod
    async def _greet(member: Member, after: VoiceState) -> None:
        """
        Helper method to greet a given member.
        :param member: The given member.
        :param after: The given information to retrieve the channel in which to join and greet.
        """
        channel = after.channel
        user = read_user_by_id(member.name)
        msg = random.choice(user.msgs)
        tts = gTTS(msg)
        tts.save("tts.mp3")
        await HolyGreetingsBot._play(channel)

    @staticmethod
    async def _play(channel, track: str = "./tts.mp3") -> None:
        """
        Helper method to play a given .mp3 file.
        :param channel: The to play in.
        :param track: Path to the track.
        """
        voice_client = await channel.connect(reconnect=False)
        audio_source = await discord.FFmpegOpusAudio.from_probe(track)
        voice_client.play(audio_source)
        while voice_client.is_playing():
            continue
        await voice_client.disconnect()

    @staticmethod
    async def _add_greet(new_msg: str, u_id: str) -> None:
        """
        Helper method to add the given greeting for the given user.
        :param msg: The given greeting.
        :param u_id: The given user id.
        """
        user = read_user_by_id(u_id)
        if user is None:
            user = User(u_id, list())
        if new_msg not in user.msgs:
            user.msgs.append(new_msg)
        write(user)

    @staticmethod
    async def _drop_greet(msg: str, u_id: str) -> None:
        """
        Helper method to drop the given greeting for the given user.
        :param msg: The given greeting.
        :param u_id: The given user id.
        """
        user = read_user_by_id(u_id)
        if user is None or msg not in user.msgs:
            return
        user.msgs.remove(msg)
        write(user)

    @staticmethod
    async def _info_greet(u_id: str, channel: TextChannel) -> None:
        """
        Helper method for printing info for the given user id in the given channel.
        :param u_id: The given user id.
        :param channel: The given channel.
        """
        user = read_user_by_id(u_id)
        if user is None or user.msgs is None or user.msgs == list():
            await HolyGreetingsBot._write_to_channel(f"No greetings found for {u_id}!", channel)
        else:
            await HolyGreetingsBot._write_to_channel(f"For '{u_id}' the following greetings have been found: {chr(10)}"
                                                     + f"{chr(10).join('- ' + msg for msg in user.msgs)}", channel)

    @staticmethod
    async def _write_to_channel(msg: str, channel: TextChannel) -> None:
        """
        Write a given message to the given channel.
        :param msg: The given message.
        :param channel: The given channel.
        """
        await channel.send(msg)
