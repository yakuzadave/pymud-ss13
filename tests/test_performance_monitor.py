import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from performance import PerformanceMonitor


def test_monitor_collects_metrics():
    mon = PerformanceMonitor(interval=0.1)
    mon.start()
    time.sleep(0.25)
    mon.stop()
    metrics = mon.metrics()
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "num_threads" in metrics
