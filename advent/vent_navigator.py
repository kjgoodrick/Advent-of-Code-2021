from pathlib import Path
import numpy as np


class VentNavigator:
    def __init__(self, line_path: Path):
        self.line_path = line_path

    def find_overlap(self, use_diagonal_lines=False):
        with open(self.line_path, 'r') as f:
            line_strs = [l for l in f]

        # Initialize empty array for the lines 2x2xn_lines
        lines: np.ndarray = np.zeros((2, 2, len(line_strs)), dtype=int)
        for i, line_str in enumerate(line_strs):
            # Split the line into p1 and p2
            p1, p2 = line_str.split(' -> ')
            # Split p1 and p2 into their respective components and convert data
            x1, y1 = map(int, p1.split(','))
            x2, y2 = map(int, p2.split(','))
            # Save into line array
            lines[:, :, i] = np.array([[x1, y1], [x2, y2]])

        # Create the vent map, size s.t. the largest x and y values can be directly indexed
        vent_map = np.zeros((np.max(lines[:, 0, :]) + 1, np.max(lines[:, 1, :]) + 1))
        # Find orthogonal lines, vertical have identical x values and horizontal have identical y values
        vert_lines = lines[0, 0, :] == lines[1, 0, :]
        horz_lines = lines[0, 1, :] == lines[1, 1, :]
        orthogonal_lines = horz_lines + vert_lines
        # Loop through orthogonal lines and add one where they are
        for i in list(np.where(orthogonal_lines)[0]):
            x = lines[:, 0, i]
            y = lines[:, 1, i]
            vent_map[min(x):max(x)+1, min(y):max(y)+1] += 1

        if use_diagonal_lines:
            # Diagonal lines are the lines that are not orthogonal
            diagonal_lines = ~orthogonal_lines
            for i in list(np.where(diagonal_lines)[0]):
                # find the x and y values of the current line
                x = lines[:, 0, i]
                y = lines[:, 1, i]
                # find the direction of the line (positive or negative slope)
                x_sign = np.sign(x[1] - x[0])
                y_sign = np.sign(y[1] - y[0])
                # Find the x and y values that should be populated
                xs = np.arange(x[0], x[1] + x_sign, x_sign)
                ys = np.arange(y[0], y[1] + y_sign, y_sign)

                # Draw the lines
                vent_map[xs, ys] += 1

        # Sum up the intersections
        return np.sum(vent_map >= 2)
