"""
Tests for thread-safety of the ErrorCollector.
"""
import threading
from itertools import batched
from flexfail import ErrorCollector, ErrorCollectorStrategy


def test_collector_is_thread_safe_when_used_concurrently():
    """
    Collector safely handles concurrent error collecting in multiple threads.
    """
    error_collector = ErrorCollector(strategy=ErrorCollectorStrategy.try_all, autowrap=True)
    errors = [RuntimeError(f'Error #{_}') for _ in range(500)]
    threads = []

    def target(errors_to_collect):
        """Thread worker"""
        for e in errors_to_collect:
            with error_collector:
                raise e

    for _ in batched(errors, 100):
        thr = threading.Thread(target=target, args=(_,))
        threads.append(thr)
        thr.start()

    for thr in threads:
        thr.join()

    # Collected all the errors.
    assert len(error_collector.errors) == len(errors)
    assert set(errors) == set([_.data for _ in error_collector.errors])
