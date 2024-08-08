import numpy as np


class Sudoku:
    def __init__(self, board: np.ndarray, difficulty: int = None):
        assert board.shape == (9, 9), "Invalid board shape"
        self.board = board
        POSSIBLES = set(range(1, 10))
        self.row_remain_set = [POSSIBLES - set(row) for row in board]
        self.col_remain_set = [POSSIBLES - set(col) for col in board.T]
        self.block_remain_set = [
            POSSIBLES - set(board[r : r + 3, c : c + 3].flatten())
            for r in range(0, 9, 3)
            for c in range(0, 9, 3)
        ]
        self.difficulty = difficulty

    def fill(self, row: int, col: int, num: int):
        assert self.board[row, col] == 0, "Cell is already filled"
        self.board[row, col] = num
        self.row_remain_set[row].remove(num)
        self.col_remain_set[col].remove(num)
        self.block_remain_set[row // 3 * 3 + col // 3].remove(num)

    def clear(self, row: int, col: int):
        num = self.board[row, col]
        assert num != 0, "Cell is already empty"
        self.board[row, col] = 0
        self.row_remain_set[row].add(num)
        self.col_remain_set[col].add(num)
        self.block_remain_set[row // 3 * 3 + col // 3].add(num)

    def candidates(self, row: int, col: int) -> set[int]:
        c_r = self.row_remain_set[row]
        c_c = self.col_remain_set[col]
        c_b = self.block_remain_set[row // 3 * 3 + col // 3]
        return c_r & c_c & c_b

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.board])

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def _valid_row(self, i: int) -> bool:
        return len(set(self.board[i])) == 9

    def _valid_col(self, i: int) -> bool:
        return len(set(self.board[:, i])) == 9

    def _valid_square(self, i: int) -> bool:
        r, c = i // 3 * 3, i % 3 * 3
        return len(set(self.board[r : r + 3, c : c + 3].flatten())) == 9

    def valid(self) -> bool:
        return all(
            self._valid_row(i) and self._valid_col(i) and self._valid_square(i)
            for i in range(9)
        )
