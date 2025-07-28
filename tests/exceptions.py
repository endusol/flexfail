"""
Tests for the exceptions used in flexfail.
"""
from flexfail.exceptions import FlexFailException


def test_exception_contains_passed_data():
    """ErrorCollectorException contains and exposes the passed data via the ``data`` property."""
    data = {'a': 100, 'b': None, 'c': 13.13, 'd': 'some-string', 'e': [1, 2, 3]}
    exception = FlexFailException(data=data)
    assert exception.data is data
