from advent.diagnostics import Diagnostics
from pathlib import Path

diag = Diagnostics(Path('../data/diagnostics/diagnostics3.txt'))
print(f'Power Consumption: {diag.power_consumption}')
print(f'Life Support Rating: {diag.life_support_rating}')
