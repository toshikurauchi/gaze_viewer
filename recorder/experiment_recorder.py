from datetime import datetime
import time
from pathlib import Path
import csv
import cv2


GAZE_FILENAME = 'gaze.csv'
MOUSE_FILENAME = 'mouse.csv'
SCREEN_FILENAME = 'screen.avi'
SCREEN_TSTAMPS_FILENAME = 'screen.csv'


class CSVWriter:
    def __init__(self, filename, header):
        self.file = open(filename, 'w')
        self.csv_file = csv.writer(self.file)
        self.csv_file.writerow(header)

    def close(self):
        self.csv_file = None
        self.file.close()

    def writerow(self, row):
        try:
            if self.csv_file:
                self.csv_file.writerow(row)
        except ValueError:
            pass  # File was already closed, which means we are losing this line


class VideoWriter:
    def __init__(self, filename, width, height):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter(str(filename), fourcc, 30.0, (width, height))

    def close(self):
        self.out.release()

    def add_frame(self, frame):
        self.out.write(frame)


class ExperimentRecorder:
    def __init__(self, participant_id, project_id, experiment_dir, screen_capturer, eye_tracker):
        self.t0 = time.time()
        self.participant_id = participant_id
        self.project_id = project_id

        now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.trial_path = Path(experiment_dir) / f'proj_{self.project_id}' / f'part_{self.participant_id}' / f'trial_{now}'
        self.trial_path.mkdir(parents=True)
        self.gaze_file = CSVWriter(self.trial_path / GAZE_FILENAME, ['tstamp', 'x', 'y'])
        self.mouse_file = CSVWriter(self.trial_path / MOUSE_FILENAME, ['tstamp', 'x', 'y'])
        self.screen_tstamps_file = CSVWriter(self.trial_path / SCREEN_TSTAMPS_FILENAME, ['tstamp'])
        self.screen_file = None

        self.screen_capturer = screen_capturer
        self.screen_capturer.add_listener(self)

        self.eye_tracker = eye_tracker
        self.eye_tracker.add_listener(self)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()

    def now(self):
        return time.time() - self.t0

    def start(self):
        pass

    def stop(self):
        self.gaze_file.close()
        self.mouse_file.close()
        self.screen_tstamps_file.close()
        if self.screen_file:
            self.screen_file.close()

    def on_gaze(self, sample):
        self.gaze_file.writerow([sample.tstamp - self.t0, sample.x, sample.y])

    def on_mouse(self, position):
        self.mouse_file.writerow([self.now(), *position])

    def on_screen(self, screen):
        height, width = screen.shape[:2]
        if not self.screen_file:
            self.screen_file = VideoWriter(self.trial_path / SCREEN_FILENAME, width, height)
        self.screen_tstamps_file.writerow([self.now()])
        self.screen_file.add_frame(screen)


class DummyRecorder:
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return

    def on_mouse(self, position):
        pass
