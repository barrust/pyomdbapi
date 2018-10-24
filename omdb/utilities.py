''' A utilitites suite '''


def camelcase_to_snake_case(_input):
    ''' Convert a camel case string to a snake case string: CamelCase -> camel_case

        Args:
            _input (str): The string to convert '''
    # https://codereview.stackexchange.com/a/185974
    res = _input[0].lower()
    for i, letter in enumerate(_input[1:], 1):
        if letter.isupper():
            try:
                if _input[i - 1].islower() or _input[i + 1].islower():
                    res += '_'
            except IndexError:
                pass
        res += letter.lower()
    return res


def range_inclusive(start, end, step=1):
    ''' Return the range of elements inclusive of the end value

        Args:
            start (int): The start value of the range
            end (int): The end value of the range
            step (int): The step value to use
        Yields:
            int: The current value within the range
    '''
    for i in range(start, end + 1, step):
        yield i


def to_int(val):
    ''' Turn the passed in variable into an int; returns 0 if errors

        Args:
            val (str): The variable to turn into an int
        Returns:
            int: The int value if possible, 0 if an error occurs
    '''
    try:
        return int(val)
    except ValueError:
        return 0
