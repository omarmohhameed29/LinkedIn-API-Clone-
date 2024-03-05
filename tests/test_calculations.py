from app.calculations import add
import pytest

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_answer(num1, num2, expected):
    print("testing")
    assert add(num1, num2) == expected