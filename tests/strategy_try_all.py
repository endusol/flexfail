"""
Tests of the `try_all` strategy.
"""
from flexfail import ErrorCollector, ErrorCollectorStrategy


def test_try_all_strategy_using_context_approach():
    """
    Tests that all errors collected using the context approach.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.try_all, autowrap=True)
    errors = [RuntimeError(f'Error #{_}') for _ in range(10)]

    for e in errors:
        with error_collector:
            raise e

    assert len(error_collector.errors) == len(errors)
    for idx, e in enumerate(error_collector.errors):
        assert errors[idx] == e.data


def test_try_all_strategy_using_decorator_approach():
    """
    Tests that all errors collected using the decorator approach.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.try_all, autowrap=True)
    errors = [RuntimeError(f'Error #{_}') for _ in range(10)]

    @error_collector
    def fn(_):
        """Wrappable."""
        raise _

    for e in errors:
        fn(e)

    assert len(error_collector.errors) == len(errors)
    for idx, e in enumerate(error_collector.errors):
        assert errors[idx] == e.data