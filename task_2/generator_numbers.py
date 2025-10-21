from typing import Generator, Callable


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Analyzes the text by splitting it by spaces, and returns the real numbers
    as a generator.

    Args:
        text (str): The input text string.

    Yields:
        float: The found real number.
    """
    for token in text.split():
        try:
            # Try to convert the token to a real number (float)
            # If the conversion is successful, this is our income number
            yield float(token)
        except ValueError:
            # If a ValueError occurs (the token is not a number, but a word,
            # punctuation, etc.), simply ignore it and move to the next token.
            continue


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Calculates the total sum of numbers (profit) in the input string,
    using the generator function.

    Args:
        text (str): The input text string.
        func (Callable): The generator function (generator_numbers) that returns numbers.

    Returns:
        float: The total sum of the numbers.
    """
    return sum(func(text))
