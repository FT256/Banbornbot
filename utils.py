import typing
import random as rnd

def get_restriction_time(string: str) -> typing.Optional[int]:
    """
    Get user restriction time in seconds
    :string: string to check for multiplier. The last symbol should be one of:
        "m" for minutes, "h" for hours and "d" for days
    :return: number of seconds to restrict or None if error
    """
    suffix={ #suffixes which can be converted to seconds are here
        'm': 60,
        'h': 3600,
        'd': 86400
    }
    string=string.replace(' ','') # remove spaces
    if string=='lucky':  # randomised mute time 4 hours max
        return rnd.randint(1, 240) * 60 # return random seconds immediately
    number, letter = string[:-1], string[-1:] # separation of number and suffix
    if number.isdigit() and letter in suffix: # if number contains only digits and letter can be converted to seconds
        return int(number) * suffix[letter] # convert number to seconds
    return None # if string is not correct we come here and return None
