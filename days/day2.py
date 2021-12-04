from advent.submarine import Submarine
from pathlib import Path

# Part 1 functionality removed from code
submarine = Submarine()
submarine.file_navigate(Path("../data/commands/commands2.txt"))
print(f"Depth: {submarine.depth}, Position: {submarine.position}, Mult: {submarine.position * submarine.depth}")
