"""
Tests of the `fail_fast` strategy.
"""
import pytest

from flexfail import ErrorCollector, ErrorCollectorStrategy
from flexfail.exceptions import FailFastException


def test_skip_strategy_using_context_approach():
    """
    Tests that none errors collected using the context approach.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.fail_fast, autowrap=True)
    errors = [RuntimeError(f'Error #{_}') for _ in range(10)]

    with pytest.raises(FailFastException):
        for e in errors:
            print(e)
            with error_collector:
                raise e

    assert len(error_collector.errors) == 1
    assert error_collector.errors[0].data is errors[0]


def test_skip_strategy_using_decorator_approach():
    """
    Tests that non errors collected using the decorator approach.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.fail_fast, autowrap=True)
    errors = [RuntimeError(f'Error #{_}') for _ in range(10)]

    @error_collector
    def fn(_):
        """Wrappable."""
        raise _

    with pytest.raises(FailFastException):
        for e in errors:
            fn(e)

    assert len(error_collector.errors) == 1
    assert error_collector.errors[0].data is errors[0]