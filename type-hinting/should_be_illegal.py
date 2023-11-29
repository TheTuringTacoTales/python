from typing import Callable, Optional, TypeVar, Union

# Define a type variable that can be an int, float, or complex
Numeric = int | float | complex


def multiply(a: Numeric, b: Numeric) -> Numeric:
    return a * b

def wrapper(func: Callable[[Numeric, Numeric], Numeric]) -> Callable[[Numeric, Numeric], Optional[Numeric]]:
    def inner(a: Numeric, b: Numeric) -> Optional[Numeric]:
        if a == 0 or b == 0:
            print("cannot multiply by zero")
            return None  # Returning 0 instead of None
        else:
            return func(a, b)

    return inner


def process_numbers(a: Numeric, b: Numeric) -> Optional[Numeric]:
    multiplier = wrapper(multiply)
    match multiplier(a, b):
        case None: # This match all is required to convince the type checker the match is exhaustive
            print("Multiplication by zero isn't allowed")
            return None
        case int(result):
            return result

# Example calls
result_int = process_numbers(5, 3)        # int
result_float = process_numbers(2.5, 3.0)  # float
result_complex = process_numbers(1 + 2j, 2 - 3j)  # complex
