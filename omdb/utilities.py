"""A utilitites suite"""


def camelcase_to_snake_case(_input: str) -> str:
    """Convert a camel case string to a snake case string: CamelCase -> camel_case

    Args:
        _input (str): The string to convert"""
    # https://codereview.stackexchange.com/a/185974
    res = _input[0].lower()
    for i, letter in enumerate(_input[1:], 1):
        if letter.isupper():
            try:
                if _input[i - 1].islower() or _input[i + 1].islower():
                    res += "_"
            except IndexError:
                pass
        res += letter.lower()
    return res


def range_inclusive(start: int, end: int, step: int = 1):
    """Return the range of elements inclusive of the end value

    Args:
        start (int): The start value of the range
        end (int): The end value of the range
        step (int): The step value to use
    Yields:
        int: The current value within the range
    """
    yield from range(start, end + 1, step)


def to_int(val: str) -> int:
    """Turn the passed in variable into an int; returns 0 if errors

    Args:
        val (str): The variable to turn into an int
    Returns:
        int: The int value if possible, 0 if an error occurs
    """
    try:
        return int(val)
    except ValueError:
        return 0


def clean_up_strings(val: str) -> str:
    hypens = [
        "\u002d",
        "\u007e",
        "\u00ad",
        "\u058a",
        "\u05be",
        "\u1400",
        "\u1806",
        "\u2010",
        "\u2011",
        "\u2012",
        "\u2013",
        "\u2014",
        "\u2015",
        "\u2053",
        "\u207b",
        "\u208b",
        "\u2212",
        "\u2e17",
        "\u2e3a",
        "\u2e3b",
        "\u301c",
        "\u3030",
        "\u30a0",
        "\ufe31",
        "\ufe32",
        "\ufe58",
        "\ufe63",
        "\uff0d",
    ]
    hypens_dd = {ord(c): "-" for c in hypens}
    return val.translate(hypens_dd)
