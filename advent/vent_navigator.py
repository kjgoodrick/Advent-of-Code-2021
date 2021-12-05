from pathlib import Path

import numpy
import numpy as np


class VentNavigator:
    def __init__(self, line_path: Path):
        self.line_path = line_path

    def find_overlap(self, use_diagonal_lines=False):
        with open(self.line_path, 'r') as f:
            line_strs = [l for l in f]

        lines: np.ndarray = np.zeros((2, 2, len(line_strs)), dtype=int)
        for i, line_str in enumerate(line_strs):
            p1, p2 = line_str.split(' -> ')
            x1, y1 = map(int, p1.split(','))
            x2, y2 = map(int, p2.split(','))
            lines[:, :, i] = np.array([[x1, y1], [x2, y2]])

        vent_map = np.zeros((np.max(lines[:, 0, :]) + 1, np.max(lines[:, 1, :]) + 1))
        vert_lines = lines[0, 0, :] == lines[1, 0, :]
        horz_lines = lines[0, 1, :] == lines[1, 1, :]
        orthogonal_lines = horz_lines + vert_lines
        for i in list(np.where(orthogonal_lines)[0]):
            x = lines[:, 0, i]
            y = lines[:, 1, i]
            vent_map[min(x):max(x)+1, min(y):max(y)+1] += 1

        if use_diagonal_lines:
            diagonal_lines = ~orthogonal_lines
            for i in list(np.where(diagonal_lines)[0]):
                x = lines[:, 0, i]
                y = lines[:, 1, i]
                x_sign = np.sign(x[1] - x[0])
                y_sign = np.sign(y[1] - y[0])
                xs = np.arange(x[0], x[1] + x_sign, x_sign)
                ys = np.arange(y[0], y[1] + y_sign, y_sign)

                vent_map[xs, ys] += 1

        return np.sum(vent_map >= 2)


if __name__ == '__main__':
    # nav = VentNavigator(Path('../data/vent_navigator/test5.txt'))
    nav = VentNavigator(Path('../data/vent_navigator/vent5.txt'))
    print(nav.find_overlap())
    print(nav.find_overlap(use_diagonal_lines=True))

