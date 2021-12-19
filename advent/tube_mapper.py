from pathlib import Path
import numpy as np


class TubeMapper:
    def __init__(self, tube_map: np.ndarray):
        self.tube_map = tube_map

    @property
    def low_mask(self):
        peak_value = np.max(self.tube_map)
        right_diff = -np.diff(self.tube_map, axis=1, append=peak_value + 1)
        left_diff = np.diff(self.tube_map, axis=1, prepend=peak_value + 1)
        top_diff = np.diff(self.tube_map, axis=0, prepend=peak_value + 1)
        bottom_diff = -np.diff(self.tube_map, axis=0, append=peak_value + 1)

        low_mask = np.logical_and.reduce([a < 0 for a in [right_diff, left_diff, top_diff, bottom_diff]])

        return low_mask

    @property
    def risk_level(self):
        return (self.tube_map + 1) * self.low_mask

    @property
    def aggregate_risk(self):
        return np.sum(self.risk_level)

    @property
    def basin_sizes(self) -> list[int]:
        minima: list[tuple[int, int]] = list(zip(*np.where(self.low_mask)))

        return [self.basin_size(minimum)[0] for minimum in minima]

    def basin_size(self, minima: tuple[int, int], basin_size: int = 1,
                   basin: set[tuple[int, int]] = None) -> tuple[int, set[tuple[int, int]]]:
        if basin is None:
            basin = {minima}
        v, h = minima
        minima_height = self.tube_map[v][h]
        for vd, hd in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nv = v + vd
            nh = h + hd
            if nv < 0 or nh < 0 or (nv, nh) in basin:
                continue
            try:
                height = self.tube_map[nv][nh]
            except IndexError:
                continue

            if 9 > height >= minima_height:
                basin_size, basin = self.basin_size((nv, nh), basin_size=basin_size + 1, basin=basin | {(nv, nh)})

        return basin_size, basin

    @property
    def largest_basin_prod(self):
        return np.product(sorted(self.basin_sizes)[-3:])

    @classmethod
    def from_file(cls, tube_map_file: Path):
        return cls(np.genfromtxt(tube_map_file, dtype=int, delimiter=1))


if __name__ == "__main__":
    # tube_mapper = TubeMapper.from_file(Path('../data/tubes/test9.txt'))
    tube_mapper = TubeMapper.from_file(Path('../data/tubes/tube9.txt'))
    print(tube_mapper.aggregate_risk)
    print(tube_mapper.largest_basin_prod)
