from threading import Thread
import time
import pyautogui


class EyeTracker:
    def __init__(self, tracker_driver):
        self.data = []
        self.running = False
        self.gaze_thread = None
        self.driver = tracker_driver

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()

    def start(self):
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
            time.sleep(0.02)
            new_data = self.driver.pop_data()
            if new_data:
                self.data += new_data


class MouseTrackerDriver:
    def pop_data(self):
        return [pyautogui.position()]


if __name__ == '__main__':
    with EyeTracker(MouseTrackerDriver()) as eye_tracker:
        for i in range(1000):
            while not eye_tracker.data:
                time.sleep(1)
            print(eye_tracker.data.pop())
