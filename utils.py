import typing
import random as rnd


def get_restriction_time(string: str) -> typing.Optional[int]:
    """
    Get user restriction time in seconds

    :string: string to check for multiplier. The last symbol should be one of:
        "m" for minutes, "h" for hours and "d" for days
    :return: number of seconds to restrict or None if error
    """
    if string == "lucky": # randomised mute time 4 hours max
        string = str(rnd.randint(1, 240)) + "m"
    if len(string) < 2:
        return None
    letter = string[-1]
    try:
        number = int("".join(c for c in string if c.isdecimal()))
    except TypeError:
        return None
    else:
        if letter == "m":
            return 60 * number
        elif letter == "h":
            return 3600 * number
        elif letter == "d":
            return 86400 * number
        else:
            return None
