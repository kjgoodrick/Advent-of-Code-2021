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

    def test_puzzle(self):
        diagnostics = Diagnostics(Path('../data/diagnostics/diagnostics3.txt'))
        assert diagnostics.gamma * diagnostics.epsilon == 4191876
