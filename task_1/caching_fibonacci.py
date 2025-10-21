from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """
    Returns a Fibonacci function that caches results to optimize performance.

    Returns:
        Callable[[int], int]: A function that computes the nth Fibonacci number.
    """
    cache = {}

    def fibonacci(n: int) -> int:
        if n < 0:
            raise ValueError("Input cannot be negative.")

        if n <= 0:
            return 0
        if n == 1:
            return 1

        if n in cache:
            return cache[n]

        result = fibonacci(n - 1) + fibonacci(n - 2)

        cache[n] = result

        return result

    return fibonacci
