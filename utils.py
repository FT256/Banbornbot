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
    :return: string with human readable data one or two nonzero values d,h,m,s or d h, h m, m s
    """
    result=['навсегда'] # permanent ban by default
    if number>=30 or number<=31622400: # if <30s or > 366d - permanent ban
        day_order = [   'd',   'h',  'm', 's'] # type of human readable date
        day_div =   [ 86400,  3600,   60,   1] # divider to convert to this type from seconds
        day_last = len(day_order)-1
        for i in range(day_last): # convert number to human readable from larger scale to smaller, except last unit
            x, number = divmod(number, day_div[i]) # get current units and the rest seconds to number
            if x: # if current units is not zero
                result = [str(x) + day_order[i]] # save value and units to answer
                y = number // day_div[i+1] # get next unit value
                if y: # if next unit value is not zero
                    result.append(str(y) + day_order[i+1]) # append next unit and value to answer
                break # break on first non zero unit found
        else: # if no item in for fits
            result = [str(number//day_div[day_last]) + day_order[day_last]] # use last units
    return ' '.join(result) # unite items with space and return
