import cv2


WIN_NAME = 'Gaze'
FRAME_TRACK = 'Frame'


class VideoPlayer:
    def play(self, frames):
        self.frame_idx = 0
        cv2.namedWindow(WIN_NAME)
        cv2.createTrackbar(FRAME_TRACK, WIN_NAME, 0, len(frames), self.set_frame_idx)

        play = False
        while self.frame_idx < len(frames):
            cv2.imshow(WIN_NAME, frames[self.frame_idx])
            cv2.setTrackbarPos(FRAME_TRACK, WIN_NAME, self.frame_idx)
            key = cv2.waitKey(30)
            if key == ord('q'):
                break
            if key == ord(' '):
                play = not play
            if play:
                self.frame_idx += 1

    def set_frame_idx(self, idx):
        self.frame_idx = idx
