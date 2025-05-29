import pytest


@pytest.mark.parametrize("dummy", list(range(10)))
def test_dummy(dummy):
    assert dummy < 10
