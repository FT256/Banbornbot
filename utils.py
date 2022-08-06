import typing

def get_restriction_time(string: str) -> typing.Optional[int]:
    """
    Get user restriction time in seconds

    :param string: string to check for multiplier. The last symbol should be one of:
        "m" for minutes, "h" for hours and "d" for days
    :return: number of seconds to restrict or None if error
    """
    if len(string) < 2:
        return None
    letter = string[-1]
    try:
        number = int(string[:-1])
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

