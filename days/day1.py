from advent.sonar import Sonar
from pathlib import Path

sonar = Sonar(Path("../data/sonar/sonar1.txt"), window_size=1)
sonar.read_sonar()
print(f'Part 1: {sonar.increases}')

sonar.window_size = 3
sonar.read_sonar()
print(f'Part 2: {sonar.increases}')
