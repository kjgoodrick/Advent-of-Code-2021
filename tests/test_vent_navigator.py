from unittest import TestCase
from pathlib import Path
from advent.vent_navigator import VentNavigator


class TestVentNavigator(TestCase):
    def setUp(self) -> None:
        self.test_nav = VentNavigator(Path('../data/vent_navigator/test5.txt'))
        self.real_nav = VentNavigator(Path('../data/vent_navigator/vent5.txt'))

    def test_find_overlap_orthogonal(self):
        assert self.test_nav.find_overlap(use_diagonal_lines=False) == 5
        assert self.real_nav.find_overlap(use_diagonal_lines=False) == 5294

    def test_find_overlap(self):
        assert self.test_nav.find_overlap(use_diagonal_lines=True) == 12
        assert self.real_nav.find_overlap(use_diagonal_lines=True) == 21698

