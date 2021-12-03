from unittest import TestCase
from advent.submarine import Submarine
from pathlib import Path


class TestSubmarine(TestCase):
    def setUp(self) -> None:
        self.submarine = Submarine()

    def test_file_navigate(self):
        self.submarine.file_navigate(Path('../data/commands/test2.txt'))
        assert self.submarine.depth == 60
        assert self.submarine.position == 15
        assert self.submarine.depth * self.submarine.position == 900

