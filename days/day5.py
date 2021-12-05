from advent.vent_navigator import VentNavigator
from pathlib import Path

nav = VentNavigator(Path('../data/vent_navigator/vent5.txt'))
print(f'Orthogonal Only Intersections: {nav.find_overlap()}')
print(f'Intersections: {nav.find_overlap(use_diagonal_lines=True)}')
