from unittest import TestCase
from advent.sonar import Sonar
from pathlib import Path


class TestSonar(TestCase):
    def setUp(self) -> None:
        self.sonar = Sonar(Path("../data/sonar/test1.txt"))

    def test_read_sonar(self):
        self.sonar.read_sonar()
        assert self.sonar.sonar_readings == [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    def test_increases(self):
        self.sonar.read_sonar()
        assert self.sonar.increases == 7

    def test_window_increases(self):
        self.sonar.window_size = 3
        self.sonar.read_sonar()
        assert self.sonar.increases == 5
