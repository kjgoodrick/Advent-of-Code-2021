from advent.fish_projector import FishProjector
from pathlib import Path

fish_counter = FishProjector.from_file(Path('../data/fish/fish6.txt'))
print(f'Day 80 Population: {fish_counter.run_days()}')
fish_counter = FishProjector.from_file(Path('../data/fish/fish6.txt'))
print(f'Day 256 Population: {fish_counter.run_days(256)}')
