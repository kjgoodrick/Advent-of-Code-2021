from pathlib import Path
import numpy as np
from functools import lru_cache


class Diagnostics:
    def __init__(self, diagnostics_path: Path):
        self.diagnostics_path = diagnostics_path

    @property
    @lru_cache(1)
    def bin_array(self) -> np.ndarray:
        # Make array of the binary diagnostics, each bit is its own cell
        with open(self.diagnostics_path, 'r') as f:
            bin_strs = [l for l in f]

        bin_rows = [[int(d) for d in bin_str.strip()] for bin_str in bin_strs]
        bin_array = np.vstack(bin_rows)

        return bin_array

    @staticmethod
    def bin_array_to_dec(bin_array: np.ndarray):
        return int(np.sum(bin_array * np.array([2**i for i in range(len(bin_array))][::-1])))

    @property
    def gamma_bin(self):
        # Counts the bits in each column and returns the most common digit in each
        ones_count = np.sum(self.bin_array, axis=0)
        return ones_count > self.bin_array.shape[0] / 2

    @property
    def gamma(self) -> int:
        return self.bin_array_to_dec(self.gamma_bin)

    @property
    def epsilon(self) -> int:
        return self.bin_array_to_dec(~self.gamma_bin)

    @property
    def power_consumption(self) -> int:
        return self.gamma * self.epsilon

    @staticmethod
    def most_common_value(bin_array: np.ndarray, index: int):
        ones_count = np.sum(bin_array, axis=0)
        most_common = ones_count >= bin_array.shape[0] / 2

        return int(most_common[index])

    def most_least_common_stepper(self, use_least_common=True):
        bin_array = self.bin_array
        for index in range(self.bin_array.shape[1]):
            most_common = self.most_common_value(bin_array, index)
            bin_array = bin_array[(bin_array[:, index] == most_common) ^ use_least_common, :]
            if bin_array.shape[0] == 1:
                return self.bin_array_to_dec(bin_array[0])
        else:
            raise RuntimeError("Something has gone wrong...")

    @property
    def oxygen_generator_rating(self) -> int:
        return self.most_least_common_stepper(use_least_common=False)

    @property
    def co2_scrubber_rating(self) -> int:
        return self.most_least_common_stepper(use_least_common=True)

    @property
    def life_support_rating(self) -> int:
        return self.oxygen_generator_rating * self.co2_scrubber_rating


if __name__ == '__main__':
    diag = Diagnostics(Path('../data/diagnostics/diagnostics3.txt'))
    print(diag.power_consumption)
    print(diag.life_support_rating)

