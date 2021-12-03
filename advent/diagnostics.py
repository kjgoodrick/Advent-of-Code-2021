from pathlib import Path
import numpy as np
from functools import lru_cache


class Diagnostics:
    def __init__(self, diagnostics_path: Path):
        self.diagnostics_path = diagnostics_path

    @property
    @lru_cache(1)
    def bin_array(self):
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
        ones_count = np.sum(self.bin_array, axis=0)
        return ones_count > self.bin_array.shape[0] / 2

    @property
    def gamma(self) -> int:
        return self.bin_array_to_dec(self.gamma_bin)

    @property
    def epsilon(self) -> int:
        return self.bin_array_to_dec(~self.gamma_bin)


if __name__ == '__main__':
    diag = Diagnostics(Path('../data/diagnostics/diagnostics3.txt'))
    print(diag.gamma * diag.epsilon)

