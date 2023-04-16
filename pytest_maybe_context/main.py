from collections.abc import Generator
from contextlib import AbstractContextManager, contextmanager
from typing import TypeGuard, TypeVar

ContextValueType = TypeVar('ContextValueType')
NonContextType = TypeVar('NonContextType')


@contextmanager
def maybe_context(
    expected: AbstractContextManager[ContextValueType] | object
) -> Generator[ContextValueType | None, None, None]:
    """
    If `expected` is a context, wraps the code in it and returns the
    returned value, otherwise executes the code and returns `None`.
    """
    if is_context(expected):
        value: ContextValueType
        with expected as value:
            yield value
    else:
        yield None


def is_context(
    expected: AbstractContextManager[ContextValueType] | object
) -> TypeGuard[AbstractContextManager[ContextValueType]]:
    """
    Checks if expected is a context manager.
    """
    return isinstance(expected, AbstractContextManager)


def not_context(
    expected: AbstractContextManager[object] | NonContextType
) -> TypeGuard[NonContextType]:
    """
    Checks if expected is not a context manager.
    """
    return not is_context(expected)
