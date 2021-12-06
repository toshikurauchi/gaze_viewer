import cv2
import imutils
from numpy.lib.twodim_base import eye
import pyautogui
from viewer.draw import BLUE, WHITE, draw_circle
from viewer.gaze import EyeTracker, MouseTrackerDriver
from viewer.heatmap import HeatmapPlotter
from viewer.screen import HEIGHT, WIDTH, ScreenCapturer


def run_viewer(tracker_driver, preview_width=-1, gaze_radius=10, window_name='Screen'):
    scale = 1
    if preview_width > 0:
        scale = preview_width / WIDTH
    preview_width = int(WIDTH * scale)
    preview_height = int(scale * HEIGHT)

    plotter = HeatmapPlotter(gaze_radius, (preview_width, preview_height))
    with ScreenCapturer() as capturer, EyeTracker(tracker_driver) as eye_tracker:
        while cv2.waitKey(1) != ord('q'):
            if capturer.screen is None:
                continue

            if preview_width > 0:
                screen = imutils.resize(capturer.screen, preview_width)
            else:
                screen = capturer.screen

            draw_circle(screen, pyautogui.position(), BLUE, 5, radius_delta=1, scale=scale)

            if eye_tracker.data:
                curr_gaze = eye_tracker.data[-1]
                draw_circle(screen, curr_gaze, WHITE, 10, radius_delta=2, scale=scale)

                while plotter.total_samples < len(eye_tracker.data):
                    plotter.add_sample(eye_tracker.data[plotter.total_samples], scale=scale)
                screen = plotter.plot(screen)

            cv2.imshow(window_name, screen)


if __name__ == '__main__':
    run_viewer(MouseTrackerDriver(), 1024, 30)
