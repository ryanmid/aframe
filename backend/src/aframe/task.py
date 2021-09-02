from typing import List, Callable
from journal import Journal, JournalEntry


def task(requirements: List[Callable[[Journal], bool]]):
    """Higher-order function that returns a decorator with associated closure containing the requirements list.

    Args:
        requirements (List[Callable[[Journal], bool]]): A list of predicates which must all return True in order
            for the decorated function to be executed
    """

    def decorator(fn: Callable[[Journal], List[JournalEntry]]):
        """A decorator for functions that take a Journal argument and return a list of JournalEntries."""

        def wrapped(journal: Journal):
            """Wrapper that intercepts calls to the wrapped function and only calls it if all predicates return True."""
            all_requirements_met = all(map(lambda predicate: predicate(journal), requirements))
            return fn(journal) if all_requirements_met else []
        return wrapped

    return decorator
