from collections import namedtuple
from threading import Thread
import time
import pyautogui
import tobii_research as tr


WIDTH, HEIGHT = pyautogui.size()
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


class TobiiTrackerDriver:
    def __init__(self):
        self.tracker = None
        self.instance = None

    def start(self):
        eyetrackers = tr.find_all_eyetrackers()
        assert len(
            eyetrackers
        ) > 0, 'Não foi encontrado nenhum eye tracker. Verifique se o eye tracker está ligado e conectado ao computador e que o TobiiProEyeTrackerManager está rodando.'
        self.instance = eyetrackers[0]
        self.instance.subscribe_to(tr.EYETRACKER_GAZE_DATA,
                                   self.on_gaze,
                                   as_dictionary=True)

    def stop(self):
        self.instance.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.on_gaze)

    def on_gaze(self, gaze_data):
        rx, ry = gaze_data['right_gaze_point_on_display_area']
        lx, ly = gaze_data['left_gaze_point_on_display_area']
        r_valid = gaze_data['right_gaze_point_validity']
        l_valid = gaze_data['left_gaze_point_validity']
        
        total = r_valid + l_valid
        if not total:
            return
        if not r_valid:
            rx, ry = 0, 0
        if not l_valid:
            lx, ly = 0, 0
        
        x = (rx * r_valid + lx * l_valid) / total * WIDTH
        y = (ry * r_valid + ly * l_valid) / total * HEIGHT
        self.tracker.add_sample(GazeData(x, y, time.time()))


if __name__ == '__main__':
    with EyeTracker(TobiiTrackerDriver()) as eye_tracker:
        time.sleep(2)