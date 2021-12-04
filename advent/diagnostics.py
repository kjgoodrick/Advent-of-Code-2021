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
    def bin_array_to_dec(bin_array: np.ndarray) -> int:
        return int(''.join(str(b) for b in bin_array), 2)

    @property
    def gamma_bin(self) -> np.ndarray:
        return self.most_common_bit(self.bin_array)

    @property
    def gamma(self) -> int:
        return self.bin_array_to_dec(self.gamma_bin)

    @property
    def epsilon(self) -> int:
        # Epsilon is gamma with all the bits flipped
        return self.bin_array_to_dec(-self.gamma_bin + 1)

    @property
    def power_consumption(self) -> int:
        return self.gamma * self.epsilon

    @staticmethod
    def most_common_bit(bin_array: np.ndarray) -> np.ndarray:
        ones_count = np.sum(bin_array, axis=0)
        return (ones_count >= bin_array.shape[0] / 2).astype(int)

    def most_least_common_stepper(self, use_least_common=True) -> int:
        # Step through the binary array keeping only the rows with the most / least common bits of the column
        # returns the decimal value of the last remaining row
        bin_array = self.bin_array
        for index in range(self.bin_array.shape[1]):
            # Find the most common bit of the reduced bit array
            most_common = self.most_common_bit(bin_array)[index]
            # Keep only the rows there the current index's digit is the most / least common
            bin_array = bin_array[(bin_array[:, index] == most_common) ^ use_least_common, :]
            # If we're down to the last row convert to int and return
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
