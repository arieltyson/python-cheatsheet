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


def demo_fixed_dates() -> None:
    # A timestamp counts seconds from the Unix epoch:
    # 1 January 1970, 00:00:00 UTC, which is second 0
    epoch = datetime.fromtimestamp(0, tz=timezone.utc)
    one_day_later = datetime.fromtimestamp(86_400, tz=timezone.utc)
    assert one_day_later - epoch == timedelta(days=1)
    assert epoch < one_day_later
    assert epoch.isoformat() == "1970-01-01T00:00:00+00:00"
    assert epoch.weekday() == 3  # Monday is 0, so a Thursday
    # The same input gives the same datetime on every run, which is
    # why tests use these instead of datetime.now()
    assert datetime.fromtimestamp(0, tz=timezone.utc) == epoch
    assert one_day_later.timestamp() == 86_400
