def capitalize_word(word):
    return word[:1].upper() + word[1:]

def remove_spaces(str: str):
    return str.replace(" ", "")

from re import sub
def spaced_to_lower_camel_case(s):
  s = remove_spaces(sub(r"(_|-)+", " ", s).title())
  return ''.join([s[0].lower(), s[1:]])

def first(iterable):
    result = first_or(iterable, None)
    if result is None:
        raise ValueError("Empty list")
    return result

def first_or_none(iterable):
    return first_or(iterable, None)
    
def first_or(iterable, if_empty):
    return next(iter(iterable), if_empty)

def _int_to_bin_str(number, power):
    return "{0:b}".format(number).rjust(power, "0")

def binary_combinations(bit_count) -> list[list[bool]]:
    return list(map(
        lambda bin_int: [ 
            True if char == "1" else False 
            for char in _int_to_bin_str(bin_int, bit_count)
        ],
        range(2**bit_count)
    ))


def chop(given_list: list, chunk_length: int):
    '''splits given list into list of lists of equal length (equal up until last list with remainder elements) '''
    return [
        given_list[chunk_start : chunk_start + chunk_length] 
        for chunk_start in range(0, len(given_list), chunk_length) 
    ]
    
def clear_console():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")