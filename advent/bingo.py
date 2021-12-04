from pathlib import Path
import numpy as np
import typing as tp


class Bingo:
    def __init__(self, numbers: tp.List[int], boards: tp.List[np.ndarray]):
        self.numbers = numbers
        self.boards = boards

        self.called_numbers = []
        self.called_masks = []

        self.generate_masks()

    def play_bingo(self, lose=False) -> int:
        # Keep track of the boards that have not won yet
        losing_boards = list(range(len(self.boards)))
        # Until we find the winning or losing board keep looping
        while True:
            # Call a number
            self.call_number()
            # Score the boards
            scores = self.score()
            # Check if any of the scores are winning
            for i, score in enumerate(scores):
                if score > 0:
                    # If we want to win we should choose this board
                    if not lose:
                        return score * self.called_numbers[-1]
                    else:
                        # If we want to lose we should remove this board from the list of losing boards
                        try:
                            losing_boards.pop(losing_boards.index(i))
                        except ValueError:
                            # No problem if we've already removed it
                            pass
                        if not losing_boards:
                            # If we've removed all the boards the most recent was the losing board
                            return score * self.called_numbers[-1]

    def generate_masks(self):
        # To keep track of which squares for each board have been called we will generate masks
        for board in self.boards:
            self.called_masks.append(np.zeros_like(board).astype(bool))

    def call_number(self):
        # Grab the next number
        called_number = self.numbers.pop(0)
        # Keep trak of the called numbers
        self.called_numbers.append(called_number)

        # Check which squares have the called number on each board
        for i, board in enumerate(self.boards):
            update_mask = board == called_number
            self.called_masks[i] += update_mask

    def score(self) -> tp.List[int]:
        scores = []
        board: np.ndarray
        mask: np.ndarray
        for board, mask in zip(self.boards, self.called_masks):
            possible_scores = []
            # Check Rows
            possible_scores.extend(np.sum(mask, axis=1))
            # Check Columns
            possible_scores.extend(np.sum(mask, axis=0))
            # Check Diagonals
            n = mask.shape[0]
            # eye = np.identity(n)
            # possible_scores.append(int(np.sum(mask * eye)))
            # possible_scores.append(int(np.sum(mask * np.rot90(eye))))

            # If any of our possible ways of winning work score the board
            if any(s == n for s in possible_scores):
                scores.append(self.score_board(board, mask))
            else:
                # Otherwise, no score
                scores.append(0)

        return scores

    @staticmethod
    def score_board(board: np.ndarray, mask: np.ndarray):
        return np.sum(board * ~mask)

    @classmethod
    def from_file(cls, bingo_path: Path):
        with open(bingo_path, 'r') as f:
            lines = [l for l in f]

        numbers = [int(n) for n in lines.pop(0).split(',')]
        lines.pop(0)
        lines.append('\n')

        boards = []
        cur_board_rows = []
        for line in lines:
            if line == '\n':
                boards.append(np.array(cur_board_rows))
                cur_board_rows = []
                continue
            cur_board_rows.append([int(n) for n in line.split()])

        return cls(numbers, boards)
