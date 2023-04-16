from contextlib import nullcontext
from warnings import warn

from pytest import mark, raises, warns
from _pytest.python_api import RaisesContext
from _pytest.recwarn import WarningsChecker

from pytest_maybe_context import maybe_context, is_context, not_context


@mark.parametrize(('buffering', 'expected'), (
    (0, open(__file__, 'rb').read()),
    (1, warns(RuntimeWarning)),
    (.1, raises(TypeError))
))
def test_example(
    buffering: int,
    expected: bytes | WarningsChecker | RaisesContext[Exception]
) -> None:
    with maybe_context(expected):
        file = open(__file__, 'rb', buffering)
    if not_context(expected):
        assert file.read() == expected


def test_maybe_context_value() -> None:
    executed = False
    with maybe_context('not_a_context') as value:
        executed = True
    assert executed and value is None


def test_maybe_context_null() -> None:
    executed = False
    with maybe_context(nullcontext()) as value:
        executed = True
    assert executed and value is None


def test_maybe_context_warns() -> None:
    with maybe_context(warns()) as warnings:
        warn("should be caught")
    assert isinstance(warnings, WarningsChecker)


def test_maybe_context_raises() -> None:
    with maybe_context(raises(RuntimeError)) as exception:
        raise RuntimeError("should be caught")
    assert exception.type == RuntimeError


def test_is_context() -> None:
    assert is_context(None) is False
    assert is_context(nullcontext) is False
    assert is_context(nullcontext()) is True


def test_not_context() -> None:
    assert not_context(None) is True
    assert not_context(nullcontext) is True
    assert not_context(nullcontext()) is False
