from pathlib import Path
import csv
import click
from player.player import VideoPlayer
from recorder.experiment_recorder import GAZE_FILENAME, MOUSE_FILENAME, SCREEN_FILENAME, SCREEN_TSTAMPS_FILENAME
import cv2
from viewer.draw import BLUE, draw_circle

from viewer.gaze import GazeData
from viewer.heatmap import HeatmapPlotter


GAZE_TYPE = 'gaze'
MOUSE_TYPE = 'mouse'
SCREEN_TYPE = 'screen'


def load_data(filename, dtype):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return [dict(**row, dtype=dtype) for row in reader]


def load_video_with_tstamps(screen_filename, screen_data):
    cap = cv2.VideoCapture(str(screen_filename))
    frame_idx = 0
    got_data = True
    while got_data:
        got_data, frame = cap.read()
        if got_data:
            if frame_idx < len(screen_data):
                screen_data[frame_idx]['frame'] = frame
                frame_idx += 1
            else:
                print('There are more frames than timestamps')
    if frame_idx < len(screen_data):
        print(f'There are fewer frames than timestamps. Found {frame_idx}.')


@click.command()
@click.argument('recording')
def view_data(recording):
    """Visualiza gravação na pasta RECORDING"""
    recording = Path(recording)
    gaze_filename = recording / GAZE_FILENAME
    mouse_filename = recording / MOUSE_FILENAME
    screen_tstamps_filename = recording / SCREEN_TSTAMPS_FILENAME
    screen_filename = recording / SCREEN_FILENAME

    screen_data = load_data(screen_tstamps_filename, SCREEN_TYPE)
    load_video_with_tstamps(screen_filename, screen_data)
    data = (
        load_data(gaze_filename, GAZE_TYPE) +
        load_data(mouse_filename, MOUSE_TYPE) +
        screen_data
    )
    data.sort(key=lambda d: d['tstamp'])

    if not screen_data:
        return
    # height, width = screen_data[0]['frame'].shape[:2]
    # plotter = HeatmapPlotter(100, (width, height), False)
    # frame = None
    # mouse = None
    # for d in data:
    #     dtype = d['dtype']
    #     if dtype == SCREEN_TYPE:
    #         frame = d
    #     if dtype == GAZE_TYPE:
    #         plotter.add_sample(GazeData(d['x'], d['y'], d['tstamp']))
    #     if dtype == MOUSE_TYPE:
    #         mouse = d['x'], d['y']
    #     if frame is not None:
    #         curr_frame = frame['frame'].copy()
    #         curr_frame = plotter.plot(curr_frame)
    #         if mouse:
    #             draw_circle(curr_frame, mouse, BLUE, 50, radius_delta=10)
    #         frame['overlayed'] = curr_frame

    VideoPlayer().play([f['frame'] for f in screen_data])


if __name__ == '__main__':
    view_data()
