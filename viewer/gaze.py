from collections import namedtuple
from threading import Thread
import time
import pyautogui


GazeData = namedtuple('GazeData', 'x, y, tstamp')


class EyeTracker:
    def __init__(self, tracker_driver):
        self.data = []
        self.listeners = []
        self.driver = tracker_driver
        self.driver.tracker = self

    def __enter__(self):
        self.driver.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.driver.stop()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def add_sample(self, sample):
        self.data.append(sample)
        for listener in self.listeners:
            listener.on_gaze(sample)


class MouseTrackerDriver:
    def __init__(self, delay=0.02):
        self.running = False
        self.gaze_thread = None
        self.tracker = None
        self.delay = delay

    def start(self):
        assert self.tracker is not None, 'Eye tracker not set'
        if self.running or self.gaze_thread:
            raise RuntimeError("Eye tracker thread started more than once")

        self.running = True
        self.gaze_thread = Thread(target=self.run)
        self.gaze_thread.start()

    def stop(self):
        self.running = False
        if self.gaze_thread:
            self.gaze_thread.join()
            self.gaze_thread = None

    def run(self):
        while self.running:
            time.sleep(self.delay)
            x, y = pyautogui.position()
            self.tracker.add_sample(GazeData(x, y, time.time()))


if __name__ == '__main__':
    with EyeTracker(MouseTrackerDriver()) as eye_tracker:
        for i in range(1000):
            while not eye_tracker.data:
                time.sleep(1)
            print(eye_tracker.data.pop())
