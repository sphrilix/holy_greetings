import os
import random
from time import sleep

from discord import Member, VoiceState, TextChannel, Attachment
from discord.ext.commands import Bot, Context
import discord
from gtts import gTTS
from gtts import lang

import json_handler
from src.main.python.greet import Greet
from json_handler import read_user_by_id, write
from mp3_greet import MP3Greet
from play_options import PlayOption, to_play_option
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
        async def info(ctx: Context, *args: str) -> None:
            """
            Send an info message about saved greetings for given u_id. If not given just get info for unknown user.
            :param ctx: Context of the command.
            :param args: Arguments of the command.
            """
            u_id = "unknown"
            for i, arg in enumerate(args[:-1]):
                if arg == "-u":
                    u_id = args[i + 1]
            await HolyGreetingsBot._write_to_channel(HolyGreetingsBot._info_greet(u_id), ctx.channel)

        @self.command(name="add")
        async def add(ctx: Context, *args: str) -> None:
            """
            Add a new given greeting for the given user id.
            :param ctx: Context of the written command.
            :param args: Arguments of the command.
            """
            language = "en"
            msg = ""
            u_id = "unknown"
            option = PlayOption.ONLY
            for i, arg in enumerate(args[:-1]):
                if arg == "-l":
                    language = args[i + 1]
                if arg == "-u":
                    u_id = args[i + 1]
                if arg == "-m":
                    msg = args[i + 1]
                if arg == "-o":
                    option = to_play_option(args[i + 1])
            if msg == "":
                await HolyGreetingsBot._write_to_channel("No message given!", ctx.channel)
            elif lang.tts_langs()[language] is None:
                await HolyGreetingsBot._write_to_channel(f"Unsupported lang: {language}!", ctx.channel)
            elif len(msg) > 500:
                await HolyGreetingsBot._write_to_channel(f"Maximum of 500 character are allowed!", ctx.channel)
            elif not ctx.message.attachments:
                await HolyGreetingsBot._write_to_channel(HolyGreetingsBot._add_greet(msg, u_id, language), ctx.channel)
            elif len(ctx.message.attachments) > 1:
                await HolyGreetingsBot._write_to_channel(f"Max one file can be appended!", ctx.channel)
            elif ctx.message.attachments[0].content_type != "audio/mpeg":
                await HolyGreetingsBot._write_to_channel(f"Only MP3-Files can be appended!", ctx.channel)
            elif ctx.message.attachments:
                await HolyGreetingsBot._write_to_channel(await HolyGreetingsBot._add_mp3_greet(
                    u_id, msg, language, ctx.message.attachments[0], option), ctx.channel)

        @self.command(name="drop")
        async def drop(ctx: Context, *args: str) -> None:
            """
            Drop a given greeting for the given user id.
            :param ctx: Context of the command.
            :param args: Arguments of the command.
            """
            msg = ""
            u_id = "unknown"
            for i, arg in enumerate(args[:-1]):
                if arg == "-u":
                    u_id = args[i + 1]
                if arg == "-m":
                    msg = args[i + 1]
            if msg == "":
                await HolyGreetingsBot._write_to_channel("No message given!", ctx.channel)
            if json_handler.read_user_by_id(u_id) is None:
                await HolyGreetingsBot._write_to_channel(f"No user found for {u_id}!", ctx.channel)
            elif len(msg) > 500:
                await HolyGreetingsBot._write_to_channel("Maximum of 500 character are allowed!", ctx.channel)
            else:
                await HolyGreetingsBot._write_to_channel(HolyGreetingsBot._drop_greet(msg, u_id), ctx.channel)

        @self.command(name="lang")
        async def lang_info(ctx: Context):
            langs = lang.tts_langs()
            await HolyGreetingsBot._write_to_channel(f"Languages: {chr(10)}"
                                                     f"{chr(10).join([f'{k}={v}' for k, v in langs.items()])}",
                                                     ctx.channel)

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
        if user is None and read_user_by_id("unknown") is None or not user.greets:
            return
        greet = random.choice(user.greets)
        if greet.file is None:
            tts = gTTS(greet.msg, lang=greet.lang)
            tts.save("./mp3/tts.mp3")
            await HolyGreetingsBot._play(channel, ("./mp3/tts.mp3", -1))
        else:
            if greet.file.option == PlayOption.ONLY or greet.msg == "":
                await HolyGreetingsBot._play(channel, (greet.file.file_path, 10))
            else:
                tts = gTTS(greet.msg, lang=greet.lang)
                tts.save("./mp3/tts.mp3")
                tracks = [("./mp3/tts.mp3", -1), (greet.file.file_path, 5)] if greet.file.option == PlayOption.END \
                    else [(greet.file.file_path, 5), ("./mp3/tts.mp3", -1)]
                await HolyGreetingsBot._play(channel, *tracks)

    @staticmethod
    async def _play(channel, *tracks: tuple[str, int]) -> None:
        """
        Helper method to play a given .mp3 file.
        :param channel: The to play in.
        :param track: Path to the track.
        """
        voice_client = await channel.connect(reconnect=False)
        for track in tracks:
            audio_source = await discord.FFmpegOpusAudio.from_probe(track[0])
            voice_client.play(audio_source)
            if track[1] < 0:
                while voice_client.is_playing():
                    continue
            else:
                sleep(track[1])
            voice_client.stop()
        await voice_client.disconnect()

    @staticmethod
    def _add_greet(new_msg: str, u_id: str, language: str) -> str:
        """
        Helper method to add the given greeting for the given user.
        :param msg: The given greeting.
        :param u_id: The given user id.
        """
        user = read_user_by_id(u_id)
        new_greet = Greet(new_msg, language)
        if user is None:
            user = User(u_id, list())
        if new_greet in user.greets:
            return f"{u_id} has already: '{new_msg}'!"
        user.greets.append(new_greet)
        write(user)
        return f"Appended '{new_msg}' for '{u_id}'."

    @staticmethod
    def _drop_greet(msg: str, u_id: str) -> str:
        """
        Helper method to drop the given greeting for the given user.
        :param msg: The given greeting.
        :param u_id: The given user id.
        """
        user = read_user_by_id(u_id)
        if user is None or msg not in [greet.msg for greet in user.greets]:
            return f"Could not drop '{msg}' for '{u_id}'! There maybe a typo in the message, since it is not present " \
                   f"for '{u_id}'!"
        else:
            greet = user.greets[user.greets.index(Greet(msg))]
            if greet.file:
                os.remove(greet.file.file_path)
            user.greets.remove(greet)
            write(user)
            return f"Dropped '{msg}' for '{u_id}'."

    @staticmethod
    def _info_greet(u_id: str) -> str:
        """
        Helper method for printing info for the given user id in the given channel.
        :param u_id: The given user id.
        """
        user = read_user_by_id(u_id)
        if user is None or user.greets is None or user.greets == list():
            return f"No greetings found for '{u_id}'!"
        else:
            return f"For '{u_id}' the following greetings have been found: {chr(10)}" \
                   f"{chr(10).join('- ' + greet.msg for greet in user.greets)}"

    @staticmethod
    async def _write_to_channel(msg: str, channel: TextChannel) -> None:
        """
        Write a given message to the given channel.
        :param msg: The given message.
        :param channel: The given channel.
        """
        await channel.send(msg)

    @staticmethod
    async def _add_mp3_greet(u_id: str, msg: str, language: str, file: Attachment, option: PlayOption) -> str:
        user = read_user_by_id(u_id)
        file_path = f"./mp3/{u_id}_{file.filename}"
        new_mp3_greet = Greet(msg, language, MP3Greet(file_path, option))
        if user is None:
            user = User(u_id, list())
        if new_mp3_greet in user.greets:
            return f"{u_id} has already: '{msg}'!"
        if file.size > 2000000:
            return f"'{file.filename}' is to big a max of 2MB are allowed."
        if len([greet for greet in user.greets if greet.file is not None]) > 2:
            return f"For '{u_id}' already two greetings with mp3 are specified!"
        user.greets.append(new_mp3_greet)
        write(user)
        await file.save(f"./mp3/{u_id}_{file.filename}")
        return f"Appended '{file.filename}' for '{u_id}'."
