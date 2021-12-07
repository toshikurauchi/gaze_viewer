from threading import Thread
import numpy as np
from mss import mss
import math
import imutils
import cv2
import time
import pyautogui


PREVIEW_WIDTH = 1024
WIDTH, HEIGHT = pyautogui.size()
SCALE = PREVIEW_WIDTH / WIDTH


class ScreenCapturer:
    def __init__(self):
        self._screen = None
        self.running = False
        self.capture_thread = None
        self.listeners = []

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()

    def start(self):
        if self.running or self.capture_thread:
            raise RuntimeError("Screen capture thread started more than once")

        self.running = True
        self.capture_thread = Thread(target=self.run)
        self.capture_thread.start()

    def stop(self):
        self.running = False
        if self.capture_thread:
            self.capture_thread.join()
            self.capture_thread = None

    def run(self):
        monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}
        with mss() as sct:
            while self.running:
                screen = np.array(sct.grab(monitor))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
                self.screen = screen

    def mouse_position(self):
        return pyautogui.position()

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, new_screen):
        if not np.array_equal(self._screen, new_screen):
            for listener in self.listeners:
                listener.on_screen(new_screen)
        self._screen = new_screen

    def add_listener(self, listener):
        self.listeners.append(listener)


if __name__ == '__main__':
    with ScreenCapturer() as capturer:
        while cv2.waitKey(1) != ord('q'):
            if capturer.screen is None:
                continue

            screen = imutils.resize(capturer.screen, PREVIEW_WIDTH)

            mouse_x, mouse_y = pyautogui.position()
            mouse_x *= SCALE
            mouse_y *= SCALE
            radius = int(5 + math.sin(time.time() * math.pi * 2))
            cv2.circle(screen, (int(mouse_x), int(mouse_y)), radius, (255, 255, 255), 1, lineType=cv2.LINE_AA)

            cv2.imshow('Screen', screen)
