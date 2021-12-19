from pathlib import Path
from bidict import bidict
from math import floor


class Navigation:
    bracket = bidict({
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    })

    def __init__(self, chunks: list[str]):
        self.chunks = chunks

    @property
    def corrupted_brackets(self) -> list[str]:
        return self.loop_brackets()[0]

    @property
    def autocomplete(self) -> list[list[str]]:
        return self.loop_brackets(autocomplete=True)

    def loop_brackets(self, autocomplete=False) -> list[list[str]]:
        corrupted = []
        autocomplete_list = []
        for chunk in self.chunks:
            bracket_list = []
            for b in chunk:
                if b in self.bracket.keys():
                    bracket_list.append(b)
                else:
                    if bracket_list[-1] != self.bracket.inv[b]:
                        corrupted.append(b)
                        break
                    else:
                        bracket_list.pop()
            else:
                autocomplete_list.append([self.bracket[b] for b in bracket_list[::-1]])
        if autocomplete:
            return autocomplete_list
        else:
            return [corrupted]

    @property
    def score_corrupted(self):
        score_dict = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }

        return sum(score_dict[b] for b in self.corrupted_brackets)

    @property
    def autocomplete_scores(self) -> list[int]:
        score_dict = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }

        scores = []
        for autocomplete in self.autocomplete:
            score = 0
            for b in autocomplete:
                score *= 5
                score += score_dict[b]
            scores.append(score)

        return scores

    @property
    def mid_autocomplete_score(self) -> int:
        scores = sorted(self.autocomplete_scores)
        return scores[floor(len(scores)/2)]

    @classmethod
    def from_file(cls, file: Path):
        with open(file, 'r') as f:
            return cls([l.strip() for l in f])


if __name__ == "__main__":
    # file_path = '../data/navigation/test10.txt'
    file_path = '../data/navigation/navigation10.txt'
    navigation = Navigation.from_file(Path(file_path))

    print(navigation.score_corrupted)
    print(navigation.mid_autocomplete_score)
