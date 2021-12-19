from pathlib import Path
import typing as tp
from enum import Enum
from bidict import bidict
from functools import lru_cache, cached_property


def first(s: set) -> tp.Any:
    return next(iter(s))


class Segment(Enum):
    upper = 0
    middle = 1
    lower = 2
    upper_left = 3
    upper_right = 4
    lower_left = 5
    lower_right = 6


class Digit(Enum):
    zero = set(Segment) - {Segment.middle}
    one = {Segment.upper_right, Segment.lower_right}
    two = set(Segment) - {Segment.upper_left, Segment.lower_right}
    three = set(Segment) - {Segment.upper_left, Segment.lower_left}
    four = {Segment.middle, Segment.upper_left, Segment.upper_right, Segment.lower_right}
    five = set(Segment) - {Segment.upper_right, Segment.lower_left}
    six = set(Segment) - {Segment.upper_right}
    seven = {Segment.upper, Segment.upper_right, Segment.lower_right}
    eight = set(Segment)
    nine = set(Segment) - {Segment.lower_left}


class Display:
    def __init__(self, input_digits: tp.List[str], output_digits: tp.List[str]):
        self.input_digits = input_digits
        self.output_digits = output_digits

    @property
    def int_output_list(self) -> tp.List[int]:
        return [self.classify_digit(d) for d in self.output_digits]

    @property
    def int_output(self) -> int:
        return int(''.join([str(d) for d in self.int_output_list]))

    def classify_digit(self, digit: str):
        digit_set = {self.letter_dict[l] for l in digit}
        return next(i for i, d in enumerate(Digit) if d.value == digit_set)
        # if len(digit) == 2:
        #     return 1
        # elif Digit.two == digit_set:
        #     return 2
        # elif Digit.three == digit_set:
        #     return 3
        # elif len(digit) == 4:
        #     return 4
        # elif digit == 'cdfbe':
        #     return 5
        # elif digit == 'cdfgeb':
        #     return 6
        # elif len(digit) == 3:
        #     return 7
        # elif len(digit) == 7:
        #     return 8
        # elif True:
        #     return 9
        # else:
        #     return None

    # @lru_cache
    @cached_property
    def letter_dict(self) -> bidict[str, Segment]:
        all_letters = {chr(c) for c in range(ord('a'), ord('a') + 7)}
        letter_dict = bidict()
        int_str_dict = dict()
        int_str_dict[1] = next(d_str for d_str in self.input_digits if len(d_str) == 2)
        int_str_dict[4] = next(d_str for d_str in self.input_digits if len(d_str) == 4)
        int_str_dict[7] = next(d_str for d_str in self.input_digits if len(d_str) == 3)
        int_str_dict[8] = next(d_str for d_str in self.input_digits if len(d_str) == 7)

        # The letter corresponding to the upper segment is the one in 7 but not in 1
        letter_dict[first(set(int_str_dict[7]) - set(int_str_dict[1]))] = Segment.upper

        # The upper right segment contains a letter missing from one of the length six digits, but is in 1
        missing_6 = {first(all_letters - set(d)) for d in self.input_digits if len(d) == 6}
        letter_dict[first(missing_6 & set(int_str_dict[1]))] = Segment.upper_right

        # lower right is in 1 but is not upper right
        letter_dict[first(set(int_str_dict[1]) - set(letter_dict.inv[Segment.upper_right]))] = Segment.lower_right

        # upper left is the letter that is in 6 of the digits
        letter_counter = {sum(1 for d in self.input_digits if l in d): l for l in all_letters}
        letter_dict[letter_counter[6]] = Segment.upper_left

        # lower left is in four of the digits
        letter_dict[letter_counter[4]] = Segment.lower_left

        # middle is in four and not yet found
        in_four = set(int_str_dict[4])
        not_found = all_letters - set(letter_dict.keys())
        middle_letter = first(in_four & not_found)
        letter_dict[middle_letter] = Segment.middle

        # lower is the only letter left
        lower_letter = first(not_found - set(middle_letter))
        letter_dict[lower_letter] = Segment.lower

        return letter_dict

    @property
    def count_1478(self):
        return sum(1 for d in self.int_output_list if d in {1, 4, 7, 8})

    @classmethod
    def from_str(cls, display_str: str):
        input_str, output_str = display_str.split('|')
        return cls(input_str.split(), output_str.split())

    @classmethod
    def list_from_file(cls, display_file: Path):
        with open(display_file, 'r') as f:
            return [cls.from_str(line) for line in f]


if __name__ == "__main__":
    file = Path('../data/display/display8.txt')
    disp: Display
    print(sum(disp.count_1478 for disp in Display.list_from_file(file)))
    print(sum(disp.int_output for disp in Display.list_from_file(file)))

