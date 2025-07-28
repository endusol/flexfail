"""
Fixtures.
"""
import pytest
import typing as t
from flexfail.exceptions import FlexFailException


__all__ = [
    'fxt__fn',
    'fxt__data_correct',
    'fxt__data_incorrect',
    'fxt__data_errors'
]


@pytest.fixture
def fxt__data_correct() -> t.List[int]:
    """
    Totally correct test data.
    :return: list of integers.
    """
    return list(range(10))


@pytest.fixture
def fxt__data_incorrect() -> t.List:
    """
    Partially correct test data.
    :return: list of values.
    """
    res = list(range(10))
    for idx in (4, 7, 8):
        res[idx] *= -1
    res[3] = 'some-string'
    return res


@pytest.fixture
def fxt__data_errors() -> t.List[t.Any]:
    """
    List of errors in the incorrect data.
    :return: list of errors.
    """
    errors = {
        'non-number': 'Value is not a number!',
        'below-zero': 'Value is below zero!'
    }
    return [
        FlexFailException(data={'value': 'some-string', 'err': errors['non-number']}),
        FlexFailException(data={'value': -4, 'err': errors['below-zero']}),
        FlexFailException(data={'value': -7, 'err': errors['below-zero']}),
        FlexFailException(data={'value': -8, 'err': errors['below-zero']})
    ]

@pytest.fixture
def fxt__fn() -> t.Callable[[t.Any], t.Any]:
    """
    Callable to use in collectors
    :return: callable
    """

    def fn(value):
        """
        Checks if value is a positive number and returns squared value.
        :return: squared value
        """
        if not isinstance(value, (int, float)):
            raise FlexFailException(data={'value': value, 'err': 'Value is not a number!'})
        if value < 0:
            raise FlexFailException(data={'value': value, 'err': 'Value is below zero!'})
        return value ** 2

    return fn