from unittest import TestCase
from pathlib import Path
from advent.fish_projector import FishProjector
from ddt import ddt, data, unpack


@ddt
class TestFishProjector(TestCase):
    @data(
        ('../data/fish/test6.txt', 80, 5934),
        ('../data/fish/test6.txt', 256, 26984457539),
        ('../data/fish/fish6.txt', 80, 390923),
        ('../data/fish/fish6.txt', 256, 1749945484935),
    )
    @unpack
    def test_run_days(self, file_name, days, expected_count):
        assert FishProjector.from_file(Path(file_name)).run_days(days) == expected_count
