import numpy as np
import cv2


def make_gaussian_map(radius):
    sigma = radius / 3
    size = int(radius * 6)
    if size % 2 == 0:  # Will force odd so it has a central pixel
        size += 1
    center = size // 2

    x = np.arange(0, size, 1, float)
    y = x[:, np.newaxis]

    x, y = np.meshgrid(range(-center, center + 1), range(-center, center + 1))
    dst_sq = x**2 + y**2
    denom = 2 * sigma**2

    gaussian = np.exp(-dst_sq / denom)
    return gaussian**0.5


def clip_start_end(full_start, full_end, partial_max, full_max):
    partial_start = 0
    if full_start < 0:
        if -full_start > partial_max:
            return ((0, 0), (0, 0))
        partial_start = -full_start
        full_start = 0

    partial_end = partial_max
    if full_end > full_max:
        if full_end - full_max > partial_max:
            return ((0, 0), (0, 0))
        partial_end = partial_max - (full_end - full_max)
        full_end = full_max

    return (partial_start, partial_end), (full_start, full_end)

def add_map(full_map, partial, center):
    full_h, full_w = full_map.shape[:2]
    partial_h, partial_w = partial.shape[:2]

    full_cx, full_cy = center
    partial_cx = partial_w // 2
    partial_cy = partial_h // 2

    fx_start = full_cx - partial_cx
    fx_end = full_cx + partial_cx + 1
    fy_start = full_cy - partial_cy
    fy_end = full_cy + partial_cy + 1

    (px_start, px_end), (fx_start, fx_end) = clip_start_end(fx_start, fx_end, partial_w, full_w)
    (py_start, py_end), (fy_start, fy_end) = clip_start_end(fy_start, fy_end, partial_h, full_h)

    full_map[fy_start:fy_end, fx_start:fx_end] += partial[py_start:py_end, px_start:px_end]
    return full_map


class HeatmapPlotter:
    # Each gaze point will create a gaussian with sigma = radius/3
    def __init__(self, radius, size):
        self.size = size
        self.heatmap = np.zeros((size[1], size[0]), np.float32)

        self.radius = radius
        self.new_gaze_map = make_gaussian_map(radius)
        self.total_samples = 0

        self.decay = 0.9

    def add_sample(self, sample, scale=1):
        # Decay 1% for each new sample (makes old samples disappear with time)
        self.heatmap *= self.total_samples / (self.total_samples + 1) * self.decay
        self.total_samples += 1

        x, y, _ = sample
        sample = (int(x * scale), int(y * scale))
        self.heatmap = add_map(self.heatmap, self.new_gaze_map / self.total_samples, sample)

    def plot(self, img):
        max_val = self.heatmap.max()
        if max_val < 1e-5:
            return img
        heatmap = self.heatmap / max_val * 255
        mask = self.heatmap**0.5
        mask = mask / mask.max() * 0.9
        mask = np.dstack((mask, mask, mask))
        heatmap = cv2.applyColorMap(heatmap.astype(np.uint8), cv2.COLORMAP_TURBO).astype(np.float32)
        return np.clip(img * (1 - mask) + heatmap * mask, 0, 255).astype(img.dtype)


if __name__ == '__main__':
    cv2.imshow('Map', make_gaussian_map(10))
    cv2.waitKey(0)
