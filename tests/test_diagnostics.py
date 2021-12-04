from unittest import TestCase
from advent.diagnostics import Diagnostics
from pathlib import Path


class TestDiagnostics(TestCase):
    def setUp(self) -> None:
        self.diagnostics = Diagnostics(Path('../data/diagnostics/test3.txt'))

    def test_gamma(self):
        assert self.diagnostics.gamma == 22

    def test_epsilon(self):
        assert self.diagnostics.epsilon == 9

    def test_puzzle1(self):
        diagnostics = Diagnostics(Path('../data/diagnostics/diagnostics3.txt'))
        assert diagnostics.power_consumption == 4191876

    def test_oxygen_rating(self):
        assert self.diagnostics.oxygen_generator_rating == 23

    def test_co2_rating(self):
        assert self.diagnostics.co2_scrubber_rating == 10
