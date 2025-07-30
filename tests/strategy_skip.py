"""
Tests of the `skip` strategy.
"""
from flexfail import ErrorCollector, ErrorCollectorStrategy


def test_skip_strategy_using_context_approach():
    """
    Tests that none errors collected using the context approach.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.skip, autowrap=True)
    with error_collector:
        for _ in range(10):
            assert _ < 0
    assert not error_collector.errors


def test_skip_strategy_using_decorator_approach():
    """
    Tests that none errors collected using the decorator approach.
    """
    error_collector = ErrorCollector(ErrorCollectorStrategy.skip, autowrap=True)

    @error_collector
    def fn(_):
        """Wrappable."""
        assert _ < 0

    for _ in range(10):
        fn(_)

    assert not error_collector.errors