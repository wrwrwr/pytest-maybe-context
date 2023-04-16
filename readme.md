# pytest-maybe-context

Makes it a bit easier to write warning and exception checks along other cases.

```python
from pytest import mark, raises, warns
from pytest_maybe_context import maybe_context, not_context

@mark.parametrize(('buffering', 'expected'), (
    (0, b'contents'),
    (1, warns(RuntimeWarning)),
    (.1, raises(TypeError))
))
def test_example(buffering, expected):
    with maybe_context(expected):
        file = open('file', 'rb', buffering)
    if not_context(expected):
        assert file.read() == expected
```

## Installation

```bash
poetry add pytest-maybe-context --group dev
```
