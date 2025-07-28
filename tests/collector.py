"""
Tests for the core behavior of the ErrorCollector.
"""
import pytest
from fixtures import *
from flexfail.exceptions import FailFastException
from flexfail import ErrorCollector, ErrorCollectorStrategy


def test_multiple_collectors_are_isolated(fxt__fn):
    """Multiple collector instances operate independently and do not share state."""
    error_collector_1 = ErrorCollector(fn=fxt__fn, strategy=ErrorCollectorStrategy.skip)
    error_collector_2 = ErrorCollector(fn=fxt__fn, strategy=ErrorCollectorStrategy.fail_fast)
    assert error_collector_1.errors is not error_collector_2.errors
    assert error_collector_1._lock is not error_collector_2._lock


def test_collector_callable_runs_without_errors_and_returns_result(fxt__fn):
    """Collector runs the wrapped function successfully and returns the result."""
    error_collector = ErrorCollector(fn=fxt__fn, strategy=ErrorCollectorStrategy.fail_fast)
    assert error_collector.call(10) == 100


def test_no_errors_collected_on_correct_data(fxt__fn, fxt__data_correct):
    """Collector.errors is zero length for correct data."""
    error_collector = ErrorCollector(fn=fxt__fn, strategy=ErrorCollectorStrategy.try_all)
    for _ in fxt__data_correct:
        error_collector.call(_)
    assert len(error_collector.errors) == 0


def test_try_all_strategy_collects_all_errors(fxt__fn, fxt__data_incorrect, fxt__data_errors):
    """Collector in ``try_all`` strategy collects all raised errors."""
    error_collector = ErrorCollector(fn=fxt__fn, strategy=ErrorCollectorStrategy.try_all)
    errors = fxt__data_errors
    for _ in fxt__data_incorrect:
        error_collector.call(_)
    assert len(error_collector.errors) == len(errors)
    for idx in range(len(errors)):
        assert error_collector.errors[idx].data == errors[idx].data


def test_fail_fast_strategy_stops_on_first_error(fxt__fn, fxt__data_incorrect, fxt__data_errors):
    """Collector in ``fail_fast`` strategy stops at the first raised error."""
    error_collector = ErrorCollector(fn=fxt__fn, strategy=ErrorCollectorStrategy.fail_fast)
    errors = fxt__data_errors
    with pytest.raises(FailFastException):
        for _ in fxt__data_incorrect:
            error_collector.call(_)
    assert len(error_collector.errors) == 1
    assert error_collector.errors[0].data == errors[0].data


def test_skip_strategy_ignores_errors_and_continues(fxt__fn, fxt__data_incorrect):
    """Collector in skip strategy ignores raised errors and continues processing."""
    error_collector = ErrorCollector(fn=fxt__fn, strategy=ErrorCollectorStrategy.skip)
    for _ in fxt__data_incorrect:
        error_collector.call(_)
    assert len(error_collector.errors) == 0
