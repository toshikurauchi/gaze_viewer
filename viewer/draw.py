import imutils
import math
import time
import cv2

from viewer.heatmap import HeatmapPlotter
from viewer.screen import HEIGHT, WIDTH


BLUE = (255, 0, 0)
WHITE = (255, 255, 255)


class PreviewRenderer:
    def __init__(self, capturer, eye_tracker, preview_width, gaze_radius):
        self.scale = 1
        if preview_width > 0:
            self.scale = preview_width / WIDTH

        self.capturer = capturer
        self.eye_tracker = eye_tracker
        self.preview_width = int(WIDTH * self.scale)
        self.preview_height = int(self.scale * HEIGHT)
        self.plotter = HeatmapPlotter(gaze_radius, (self.preview_width, self.preview_height))

    def draw_preview(self):
        gaze_data = self.eye_tracker.data

        if self.preview_width > 0:
            preview = imutils.resize(self.capturer.screen, self.preview_width)
        else:
            preview = self.capturer.screen

        draw_circle(preview, self.capturer.mouse_position(), BLUE, 5, radius_delta=1, scale=self.scale)

        if gaze_data:
            curr_gaze = gaze_data[-1]
            draw_circle(preview, curr_gaze[:2], WHITE, 10, radius_delta=2, scale=self.scale)

            while self.plotter.total_samples < len(gaze_data):
                self.plotter.add_sample(gaze_data[self.plotter.total_samples], scale=self.scale)
            preview = self.plotter.plot(preview)

        return preview


def draw_circle(screen, center, color, radius, radius_delta=0, pulse_freq=2*math.pi, scale=1):
    center = scale_point(center, scale)
    radius = int(radius + math.sin(time.time() * pulse_freq) * radius_delta)
    cv2.circle(screen, center, radius, color, 1, lineType=cv2.LINE_AA)


def scale_point(point, scale):
    x, y = point
    return int(scale * x), int(scale * y)
