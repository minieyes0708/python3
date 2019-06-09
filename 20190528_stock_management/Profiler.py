#  -*- encoding=utf-8 -*-
class Profiler:
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

    def stamp(self):
        import time
        self.count += 1
        self.total += (time.clock() - self.start_time)

    def remaining_time(self, left_count):
        import math
        average = self.total / self.count
        left_seconds = left_count * average
        hours = math.floor(left_seconds / 60 / 60)
        left_seconds -= hours * 60 * 60
        minutes = math.floor(left_seconds / 60)
        left_seconds -= minutes * 60
        seconds = math.floor(left_seconds)
        return (hours, minutes, seconds)
