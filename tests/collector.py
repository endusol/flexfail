"""
General tests of the ErrorCollector.
"""
from flexfail import ErrorCollector, ErrorCollectorStrategy


def test_multiple_collectors_are_isolated():
    """Multiple collector instances operate independently and do not share state."""
    error_collector_1 = ErrorCollector(strategy=ErrorCollectorStrategy.skip)
    error_collector_2 = ErrorCollector(strategy=ErrorCollectorStrategy.fail_fast)
    assert error_collector_1.errors is not error_collector_2.errors
    assert error_collector_1._lock is not error_collector_2._lock
