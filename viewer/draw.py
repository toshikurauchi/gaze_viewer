import imutils
import math
import time
import cv2
import numpy as np

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


def draw_text(image, text):
    height, width = image.shape[:2]

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 2
    color = (200, 200, 200)
    thickness = 2
    lines = text.split('\n')

    (text_width, text_height), line_offset = get_text_size(text, font, fontScale, thickness)
    orig_x = (width - text_width) // 2
    orig_y = (height - text_height) // 2

    for line in lines:
        origin = (orig_x, orig_y)
        frame = cv2.putText(image, line, origin, font, fontScale, color, thickness, cv2.LINE_AA)
        orig_y += line_offset

    return frame


def draw_rectangle(frame, corner1, corner2, color, alpha):
    if corner1 is None or corner2 is None:
        return frame

    (x1, y1), (x2, y2) = sort_corners(corner1, corner2)

    orig_dtype = frame.dtype
    frame = frame.astype(np.float32)
    frame[y1:y2+1, x1:x2+1] *= 1 - alpha
    frame[y1:y2+1, x1:x2+1] += alpha * np.array(color, dtype=frame.dtype)
    return frame.astype(orig_dtype)


def sort_corners(corner1, corner2):
    x1, y1 = corner1
    x2, y2 = corner2
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    return (x1, y1), (x2, y2)


def get_text_size(text, font, fontScale, thickness):
    lines = text.split('\n')

    text_width, text_height, line_offset = 0, 0, 0
    for line in lines:
        (line_width, line_height), _ = cv2.getTextSize(line, font, fontScale, thickness)
        text_width = max(text_width, line_width)
        line_height = int(line_height * 2.5)
        text_height += line_height
        line_offset = max(line_offset, line_height)

    return (text_width, text_height), line_offset
