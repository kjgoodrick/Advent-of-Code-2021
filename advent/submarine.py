from pathlib import Path
from enum import Enum

import typing as tp


class Direction(Enum):
    forward = 'forward'
    down = 'down'
    up = 'up'


class Command:
    def __init__(self, direction: Direction, magnitude: int):
        self.direction = direction
        self.magnitude = magnitude

    @classmethod
    def from_str_tuple(cls, str_tuple):
        direction = Direction(str_tuple[0])
        magnitude = int(str_tuple[1])

        return cls(direction, magnitude)


class Submarine:
    def __init__(self):
        self.depth = 0
        self.position = 0

    def file_navigate(self, directions_path: Path):
        with open(directions_path, 'r') as f:
            commands = [Command.from_str_tuple(line.split(' ')) for line in f]

        self.navigate(commands)

    def navigate(self, commands: tp.List[Command]):
        for command in commands:
            match command.direction:
                case Direction.forward:
                    self.position += command.magnitude
                case Direction.down:
                    self.depth += command.magnitude
                case Direction.up:
                    self.depth -= command.magnitude
                case _:
                    raise RuntimeError(f"Direction {command.direction} is not known.")


if __name__ == "__main__":
    submarine = Submarine()
    submarine.file_navigate(Path("../data/commands/commands2.txt"))
    print(f"Depth: {submarine.depth}, Position: {submarine.position}, Mult: {submarine.position * submarine.depth}")