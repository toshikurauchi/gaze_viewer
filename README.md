# Gaze Viewer

## Setup

Create a virtual env (not required, but highly recommended) and then:

    $ pip install -r requirements.txt

## Running an experiment

Run

    $ python main.py

For help:

    $ python main.py --help

## Generating video with gaze overlay

Run

    $ python main_post_process.py TRIAL_DIR

Where `TRIAL_DIR` is the directory containing the trial recorded data.
