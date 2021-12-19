from pathlib import Path

import numpy as np
import cvxpy as cp
import typing as tp


class CrabAligner:
    def __init__(self, positions: tp.List):
        self.positions = np.array(positions)
        self.num_crabs = len(positions)

    def find_fuel_use(self, linear=True):
        if linear:
            return self.linear_fuel_use()
        else:
            return self.quadratic_fuel_use()

    def linear_fuel_use(self):
        c = np.ones((self.num_crabs,))
        move = cp.Variable(self.num_crabs, integer=True)
        abs_move = cp.Variable(self.num_crabs)
        optimal_position = cp.Variable(1, integer=True)
        final_pos_con = self.positions + move == optimal_position
        prob = cp.Problem(cp.Minimize(c @ abs_move), [abs_move >= move, abs_move >= -move, final_pos_con])

        res = prob.solve(solver='ECOS_BB')

        return round(res)

    def quadratic_fuel_use(self):
        move = cp.Variable(self.num_crabs)
        # abs_move = cp.Variable(self.num_crabs)
        optimal_position = cp.Variable(1, integer=False)
        final_pos_con = self.positions + move == optimal_position
        max_position = max(self.positions)
        limit_cons = [move <= max_position, move >= -max_position, optimal_position <= max_position, optimal_position >= 0]
        cons = limit_cons + [final_pos_con]
        objective = cp.Minimize(cp.sum(cp.square(move) / 2 + cp.abs(move) / 2))
        prob = cp.Problem(objective, cons)
        # objective = cp.Minimize(cp.sum(cp.square(abs_move) / 2 + abs_move / 2))
        # prob = cp.Problem(objective, [abs_move >= move, abs_move >= -move, final_pos_con])

        fuel_use = prob.solve(verbose=True)

        opt_pos = round(optimal_position.value[0])
        real_move = self.positions - opt_pos
        real_fuel = np.sum(np.square(real_move) / 2 + np.abs(real_move) / 2)

        return round(real_fuel)

        pass

    @classmethod
    def from_file(cls, file_path: Path):
        with open(file_path, 'r') as f:
            pos_str = f.readline()

        return cls(list(map(int, pos_str.split(','))))


if __name__ == "__main__":
    aligner = CrabAligner.from_file(Path('../data/crab/crab7.txt'))
    # aligner = CrabAligner.from_file(Path('../data/crab/test7.txt'))
    print(aligner.find_fuel_use(linear=False))


