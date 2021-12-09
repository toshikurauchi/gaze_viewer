from pathlib import Path
import cv2
import click
from recorder.experiment_recorder import DummyRecorder, ExperimentRecorder
from viewer.draw import PreviewRenderer
from viewer.gaze import EyeTracker, MouseTrackerDriver, TobiiTrackerDriver
from viewer.screen import ScreenCapturer


DEFAULT_EXP_DIR = Path(__file__).parent / 'data'


@click.command()
@click.option('--id', prompt='ID do participante', help='Identificador único do participante')
@click.option('--projeto', prompt='ID do projeto', help='Identificador único do projeto')
@click.option('--experiment_dir', default=DEFAULT_EXP_DIR, help='Diretório de dados do experimento')
@click.option('--mouse', is_flag=True, help='Usar mouse')
@click.option('--record/--norecord', default=True, help='Não gravar experimento')
@click.option('--preview_width', default=1024, help='Largura da imagem de preview')
@click.option('--gaze_radius', default=30, help='Raio do indicador do olhar')
@click.option('--window_name', default='Gaze', help='Título da janela')
def run_viewer(id, projeto, experiment_dir, mouse, record, preview_width, gaze_radius, window_name):
    capturer = ScreenCapturer()
    if mouse:
        driver = MouseTrackerDriver()
    else:
        driver = TobiiTrackerDriver()
    eye_tracker = EyeTracker(driver)
    if record:
        recorder = ExperimentRecorder(id, projeto, experiment_dir, capturer, eye_tracker)
    else:
        recorder = DummyRecorder()
    with capturer, eye_tracker, recorder:
        renderer = PreviewRenderer(capturer, eye_tracker, preview_width, gaze_radius)
        while cv2.waitKey(1) != ord('q'):
            if capturer.screen is None:
                continue

            preview = renderer.draw_preview()
            recorder.on_mouse(capturer.mouse_position())

            cv2.imshow(window_name, preview)


if __name__ == '__main__':
    run_viewer()
