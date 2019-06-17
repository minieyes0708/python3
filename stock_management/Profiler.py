#  -*- encoding=utf-8 -*-
import unittest


class Profiler:
    total = 0
    count = 0
    start_time = 0

    def __init__(self):
        self.reset()

    def reset(self):
        import time
        self.total = 0
        self.count = 0
        self.start_time = time.clock()

    def start(self):
        import time
        self.start_time = time.clock()

    def stamp(self, weighting=1):
        import time
        self.count += weighting
        self.total += (time.clock() - self.start_time) * weighting

    def remaining_time(self, left_count):
        import math
        average = self.total / self.count
        left_seconds = left_count * average
        hours = math.floor(left_seconds / 60 / 60)
        left_seconds -= hours * 60 * 60
        minutes = math.floor(left_seconds / 60)
        left_seconds -= minutes * 60
        seconds = math.floor(left_seconds)
        return hours, minutes, seconds


class TestProfiler(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.profiler = Profiler()

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def testReset(self):
        import time
        self.profiler.reset()
        time.sleep(1)
        self.profiler.stamp()
        self.assertNotEqual(self.profiler.total, 0)
        self.assertNotEqual(self.profiler.count, 0)
        self.assertTrue(time.clock() - self.profiler.start_time > 0.5)
        self.profiler.reset()
        self.assertEqual(self.profiler.total, 0)
        self.assertEqual(self.profiler.count, 0)
        self.assertTrue(time.clock() - self.profiler.start_time < 0.5)

    def testStart(self):
        import time
        self.profiler.reset()
        time.sleep(1)
        self.assertTrue(time.clock() - self.profiler.start_time > 0.5)
        self.profiler.start()
        self.assertTrue(time.clock() - self.profiler.start_time < 0.5)

    def testStamp(self):
        import time
        self.profiler.reset()
        time.sleep(1)
        self.profiler.stamp()
        self.assertTrue(1.05 > self.profiler.total > 0.95, "total = {0}".format(self.profiler.total))
        self.assertTrue(self.profiler.count, 1)
        self.profiler.reset()
        time.sleep(1)
        self.profiler.stamp(2)
        self.assertTrue(2.05 > self.profiler.total > 1.95)
        self.assertTrue(self.profiler.count, 2)

    def testRemainingTime(self):
        import time
        self.profiler.reset()
        time.sleep(1)
        self.profiler.stamp()
        hour, minute, second = self.profiler.remaining_time(3)
        self.assertEqual(hour, 0)
        self.assertEqual(minute, 0)
        self.assertTrue(3.05 > second > 2.95, "second = {0}".format(second))
