import math
import time
import cv2


BLUE = (255, 0, 0)
WHITE = (255, 255, 255)


def draw_circle(screen, center, color, radius, radius_delta=0, pulse_freq=2*math.pi, scale=1):
    center = scale_point(center, scale)
    radius = int(radius + math.sin(time.time() * pulse_freq) * radius_delta)
    cv2.circle(screen, center, radius, color, 1, lineType=cv2.LINE_AA)


def scale_point(point, scale):
    x, y = point
    return int(scale * x), int(scale * y)
