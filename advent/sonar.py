import typing as tp
from pathlib import Path
import numpy as np


class Sonar:
    def __init__(self, sonar_readings_file: Path, window_size: int = 1):
        self.sonar_readings_file = sonar_readings_file
        self.window_size = window_size
        self.sonar_readings = []

    def read_sonar(self):
        # Open the file read only
        with open(self.sonar_readings_file, 'r') as f:
            # Read each line and convert to float
            for line in f:
                self.sonar_readings.append(float(line))

    @property
    def increases(self) -> int:
        # Convert readings to numpy array
        readings = np.array(self.sonar_readings)
        # For the number of elements in the rolling window (n) make a copy of the readings and shift them to the right
        # by their row. e.g. the first copy is shifted one, the second two, etc
        readings_rows = [np.roll(readings, i) for i in range(self.window_size)]
        # Stack the copies into a matrix
        stacked_reading = np.vstack(readings_rows)
        # Remove the first n-1 columns
        stacked_reading = stacked_reading[:, self.window_size-1:]
        # Sum the columns
        reading_sums = np.sum(stacked_reading, axis=0)
        # Diff the sums
        readings_diff = np.diff(reading_sums)
        # Find increase / decrease / no change
        readings_sign = np.sign(readings_diff)
        # Count changes
        sign_counts = dict(zip(*np.unique(readings_sign, return_counts=True)))
        return sign_counts[1]


if __name__ == "__main__":
    sonar = Sonar(Path("../data/sonar/sonar1.txt"), window_size=3)
    sonar.read_sonar()
    print(sonar.increases)
