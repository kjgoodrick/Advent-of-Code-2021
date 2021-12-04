from unittest import TestCase
from advent.bingo import Bingo
from pathlib import Path


class TestBingo(TestCase):
    def setUp(self) -> None:
        self.bingo = Bingo.from_file(Path('../data/bingo/test4.txt'))

    def test_play_bingo(self):
        assert self.bingo.play_bingo() == 4512

    def test_lose_bingo(self):
        assert self.bingo.play_bingo(lose=True) == 1924

    def test_puzzle(self):
        bingo = Bingo.from_file(Path('../data/bingo/bingo4.txt'))
        assert bingo.play_bingo() == 11536
        assert bingo.play_bingo(lose=True) == 1284
