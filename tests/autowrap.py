"""
Tests the autowrap functionality of ErrorCollector.
"""
import pytest

from flexfail import ErrorCollector, ErrorCollectorStrategy
from flexfail.exceptions import FlexFailException


def test_default_autowrap_is_true():
    """
    Tests that default value of autowrap is `True`.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.skip)
    assert error_collector._autowrap == True


def test_exception_is_wrapped_when_autowrap_enabled():
    """
    Tests that raised exception is wrapped if autowrap is enabled.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.try_all, autowrap=True)
    non_collectable_error = RuntimeError('Test exception!')
    with error_collector:
        raise non_collectable_error
    assert isinstance(error_collector.errors[0], FlexFailException)
    assert error_collector.errors[0].data is non_collectable_error


def test_exception_is_raised_when_autowrap_disabled():
    """
    Tests that exception (non `flexfail.exceptions.FlexFailException`) is raised if autowrap is disabled.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.try_all, autowrap=False)
    non_collectable_error = RuntimeError('Test exception!')
    with pytest.raises(RuntimeError):
        with error_collector:
            raise non_collectable_error


def test_collectable_exception_is_collected_when_autowrap_disabled():
    """
    Tests that collectable exception (`flexfail.exceptions.FlexFailException`)
    is collected even when autowrap is disabled.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.try_all, autowrap=False)
    collectable_error = FlexFailException(data={'description': 'Test exception!'})
    with error_collector:
        raise collectable_error
    assert error_collector.errors[0] is collectable_error
