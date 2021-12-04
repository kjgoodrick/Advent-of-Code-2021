from advent.bingo import Bingo
from pathlib import Path

bingo = Bingo.from_file(Path("../data/bingo/bingo4.txt"))
print(f'Winning Score: {bingo.play_bingo()}')
print(f'Losing Score: {bingo.play_bingo(lose=True)}')
