"""
Tests for thread-safety of the ErrorCollector.
"""
import threading
from fixtures import *
from itertools import batched
from flexfail import ErrorCollector, ErrorCollectorStrategy


def test_collector_is_thread_safe_when_used_concurrently(fxt__fn):
    """
    Collector safely handles concurrent error collection in multiple threads.
    """
    error_collector = ErrorCollector(strategy=ErrorCollectorStrategy.try_all, fn=fxt__fn)
    data = list(range(-1, -501, -1))
    threads = []

    def target(data_to_process):
        """Thread worker"""
        for _ in data_to_process:
            error_collector.call(_)

    for _ in batched(data, 100):
        thr = threading.Thread(target=target, args=(_,))
        threads.append(thr)
        thr.start()

    for thread in threads:
        thread.join()

    assert len(error_collector.errors) == len(data)
    sorted_errors = sorted(error_collector.errors, key=lambda _: -getattr(_, 'data')['value'])
    for idx, error in enumerate(sorted_errors):
        assert error.data == {'value': data[idx], 'err': 'Value is below zero!'}