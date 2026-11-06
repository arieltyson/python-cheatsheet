import random
import unittest
from datetime import datetime, timedelta, timezone
from threading import Thread

from snippets.structures.rolling_window import (
    RollingMax,
    RollingWindow,
    TimedValue,
)

START = datetime(2026, 1, 1, tzinfo=timezone.utc)
GENERATOR = random.Random(13)


def timed(seconds: float, value: float) -> TimedValue:
    return TimedValue(START + timedelta(seconds=seconds), value)


class RollingWindowTests(unittest.TestCase):
    def test_keeps_value_exactly_at_cutoff(self) -> None:
        window = RollingWindow(timedelta(seconds=5))
        window.append(timed(1, 5))
        window.append(timed(6, 0))
        self.assertEqual(len(window), 2)
        self.assertTrue(window.has_value(5))
        window.append(timed(6.5, 0))
        self.assertEqual(len(window), 2)
        self.assertFalse(window.has_value(5))

    def test_empty(self) -> None:
        window = RollingWindow(timedelta(seconds=5))
        self.assertEqual(len(window), 0)
        self.assertFalse(window.has_value(0))
        self.assertIsNone(RollingMax(timedelta(seconds=5)).peak())

    def test_matches_brute_force(self) -> None:
        for _ in range(50):
            duration = timedelta(seconds=GENERATOR.uniform(0, 3))
            window = RollingWindow(duration)
            rolling_max = RollingMax(duration)
            items = []
            seconds = 0.0
            for _ in range(200):
                seconds += GENERATOR.uniform(0, 1)
                item = timed(seconds, GENERATOR.randint(0, 10))
                items.append(item)
                window.append(item)
                rolling_max.append(item)

                cutoff = item.timestamp - duration
                live = [i for i in items if i.timestamp >= cutoff]
                peak = max(i.value for i in live)
                self.assertEqual(len(window), len(live))
                self.assertTrue(window.has_value(peak))
                self.assertFalse(window.has_value(peak + 0.5))
                self.assertEqual(rolling_max.peak(), peak)

    def test_parallel_appends_lose_nothing(self) -> None:
        window = RollingWindow(timedelta(seconds=5))

        def add_many() -> None:
            for _ in range(1_000):
                window.append(timed(0, 1))

        threads = [Thread(target=add_many) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(window), 8_000)


if __name__ == "__main__":
    unittest.main()
