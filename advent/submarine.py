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
        self.aim = 0

    def file_navigate(self, directions_path: Path):
        with open(directions_path, 'r') as f:
            # For each line in the file split the line on space and generate a command
            commands = [Command.from_str_tuple(line.split(' ')) for line in f]

        # Navigate with the list of commands
        self.navigate(commands)

    def navigate(self, commands: tp.List[Command]):
        for command in commands:
            match command.direction:
                # If we're going forward compute the new position and depth
                case Direction.forward:
                    self.position += command.magnitude
                    self.depth += self.aim * command.magnitude
                # If we're going down adjust the aim
                case Direction.down:
                    self.aim += command.magnitude
                # If we're going up adjust the aim up
                case Direction.up:
                    self.aim -= command.magnitude
                # If we don't see a direction we recognize, raise an error
                case _:
                    raise RuntimeError(f"Direction {command.direction} is not known.")
