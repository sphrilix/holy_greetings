from enum import Enum


class PlayOption(Enum):
    ONLY = "ONLY"
    END = "END"
    START = "START"


def to_play_option(arg: str) -> PlayOption:
    arg = arg.lower()
    if arg[0] == "e":
        return PlayOption.END
    elif arg[0] == "s":
        return PlayOption.START
    return PlayOption.ONLY
