from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import Lock


@dataclass(frozen=True)
class TimedValue:
    timestamp: datetime
    value: float


class RollingWindow:
    """Keep only the values from the last `duration`."""

    def __init__(self, duration: timedelta) -> None:
        self._duration = duration
        self._items: deque[TimedValue] = deque()
        self._lock = Lock()

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)

    def append(self, item: TimedValue) -> None:
        with self._lock:
            self._items.append(item)
            cutoff = item.timestamp - self._duration
            while self._items[0].timestamp < cutoff:
                self._items.popleft()

    def has_value(self, at_least: float) -> bool:
        with self._lock:
            return any(i.value >= at_least for i in self._items)


class RollingMax:
    """The same window, but reads the largest value in O(1)."""

    def __init__(self, duration: timedelta) -> None:
        self._duration = duration
        # Values strictly decrease from front to back
        self._candidates: deque[TimedValue] = deque()
        self._lock = Lock()

    def peak(self) -> float | None:
        with self._lock:
            if not self._candidates:
                return None
            return self._candidates[0].value

    def append(self, item: TimedValue) -> None:
        with self._lock:
            candidates = self._candidates
            # A smaller, older value can never be the largest again
            while candidates and candidates[-1].value <= item.value:
                candidates.pop()
            candidates.append(item)
            cutoff = item.timestamp - self._duration
            while candidates[0].timestamp < cutoff:
                candidates.popleft()


def demo_rolling_window() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    window = RollingWindow(timedelta(seconds=5))
    for seconds, value in [(0, 5), (4, 1), (6, 2)]:
        moment = start + timedelta(seconds=seconds)
        window.append(TimedValue(moment, value))
    # At 6 seconds the cutoff is 1 second, so the first value is gone
    assert len(window) == 2
    assert window.has_value(5) is False
    assert window.has_value(2) is True


def demo_rolling_max() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    window = RollingMax(timedelta(seconds=5))
    window.append(TimedValue(start, 5))
    window.append(TimedValue(start + timedelta(seconds=4), 1))
    assert window.peak() == 5
    window.append(TimedValue(start + timedelta(seconds=6), 2))
    assert window.peak() == 2
