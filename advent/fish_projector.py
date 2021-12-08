from pathlib import Path
from collections import defaultdict

import typing as tp


class FishProjector:
    def __init__(self, fish_list: tp.List[int]):
        self.day_counter = 0
        self.fish_counter = dict()

        self.fish_counter[self.day_counter] = defaultdict(int)
        for fish in fish_list:
            self.fish_counter[self.day_counter][fish] += 1

    def run_day(self):
        self.day_counter += 1
        self.fish_counter[self.day_counter] = defaultdict(int)
        for age, count in self.fish_counter[self.day_counter - 1].items():
            if age == 0:
                self.fish_counter[self.day_counter][6] += count
                self.fish_counter[self.day_counter][8] += count
            else:
                self.fish_counter[self.day_counter][age - 1] += count

    def run_days(self, days: int = 80) -> int:
        for i in range(days):
            self.run_day()

        return self.count_fish(days)

    def count_fish(self, day: int) -> int:
        return sum(self.fish_counter[day].values())

    @classmethod
    def from_file(cls, fish_file: Path):
        with open(fish_file, 'r') as f:
            fish_line = f.readline()

        fish_list = list(map(int, fish_line.split(',')))

        return cls(fish_list)
