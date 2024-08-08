import numpy as np
from sudoku.entity import Sudoku


class BacktrackingSolver:
    _n_iter = 0

    def __init__(self, max_iter: int = 10**8):
        self.max_iter = max_iter
        self.reset()

    def reset(self):
        BacktrackingSolver._n_iter = 0

    def solve(self, sudoku: Sudoku) -> bool:
        """
        Solve the given Sudoku puzzle using backtracking.
        """
        BacktrackingSolver._n_iter += 1
        if BacktrackingSolver._n_iter >= self.max_iter:
            raise TimeoutError(
                f"Exceeded maximum number of iterations ({self.max_iter})"
            )
        n_row, n_col = sudoku.board.shape
        random_row = np.random.permutation(n_row)
        for i in random_row:
            for j in range(n_col):
                if sudoku.board[i, j] == 0:
                    for num in sudoku.candidates(i, j):
                        sudoku.explore(i, j, num)

                        if self.solve(sudoku):
                            return True
                        sudoku.step_back(i, j)
                    return False
        return True

    def _is_valid(self, sudoku: Sudoku, row: int, col: int, num: int) -> bool:
        if num in sudoku.board[row, :]:
            return False
        if num in sudoku.board[:, col]:
            return False
        r, c = row // 3 * 3, col // 3 * 3
        if num in sudoku.board[r : r + 3, c : c + 3]:
            return False
        return True
