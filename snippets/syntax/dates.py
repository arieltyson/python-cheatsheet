import time
from datetime import datetime, timedelta, timezone


def demo_date_math() -> None:
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    window = timedelta(seconds=5)
    # Subtract a timedelta to move back: five seconds before now
    cutoff = now - window
    assert cutoff.second == 55
    # datetime - datetime gives a timedelta
    assert now - cutoff == window
    assert (now - cutoff).total_seconds() == 5.0
    assert cutoff < now


def demo_elapsed_time() -> None:
    start = time.monotonic()
    elapsed = time.monotonic() - start
    assert elapsed >= 0
