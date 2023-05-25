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

def restriction_time_to_human_readable(number: int) -> str:
    """
    Convert number of seconds to human readable date
    :number: seconds
    :return: string with human readable data
    Month is 4 weeks, not 30 days
    Year is 48 weeks and not 365 days
    """
    day_order = [  'y', 'mo', 'w', 'd', 'h', 'm', 's' ] # type of human readable date
    day_div =   [ None,   12,   4,   7,  24,  60,  60 ] # divider to convert current type to next type
    day_content={ _:0 for _ in day_order } # empty date
    for i in range(len(day_order)-1,0,-1): # convert number in reverse order to human readable
        number, day_content[ day_order[i] ] = divmod(number, day_div[i]) # get current type value and excess number for next conversion
        day_content[ day_order[i-1] ] = number # store excess number to next item
    return ' '.join([ str(day_content[day])+day for day in day_order if day_content[day] ]) # concatenate nonzero values with their names
