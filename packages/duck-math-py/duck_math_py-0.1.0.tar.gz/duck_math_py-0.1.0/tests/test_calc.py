import pytest
from duck_math_py.calc import total

def test_total():
    assert total(3, 4) == 7
    assert total(-1, 5) == 4
    assert total(0, 10) == 10
    assert total(7, 7) == 14