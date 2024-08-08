import numpy as np

from sudoku.constants import ActionType


class Action:
    def __init__(
        self,
        action_type: int,
        row: int,
        col: int,
        num: int,
        step: int,
        is_note: bool = False,
    ):
        self.action_type = action_type
        self.is_note = is_note
        self.row = row
        self.col = col
        self.num = num
        self.step = step

    def __str__(self):
        return f"{'Fill' if self.action_type else 'Clear'} ({self.row}, {self.col}) with {self.num} {'(Note)' if self.is_note else ''}"

    def __repr__(self):
        return str(self)


class ActionStack:
    def __init__(self):
        self.stack = []

    def push(self, action: Action):
        self.stack.append(action)

    def pop(self):
        return self.stack.pop()

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return str(self.stack)

    def __repr__(self):
        return str(self.stack)


class Sudoku:
    def __init__(
        self, board: np.ndarray, board_gt: np.ndarray = None, difficulty: int = None
    ):
        assert board.shape == (9, 9), "Invalid board shape"
        self.board = board
        self.origin_board = board.copy()
        self.board_gt = board_gt
        self.notes = np.array([[set() for _ in range(9)] for _ in range(9)], dtype=set)

        POSSIBLES = set(range(1, 10))
        self.row_remain_set = [POSSIBLES - set(row) for row in board]
        self.col_remain_set = [POSSIBLES - set(col) for col in board.T]
        self.block_remain_set = [
            POSSIBLES - set(board[r : r + 3, c : c + 3].flatten())
            for r in range(0, 9, 3)
            for c in range(0, 9, 3)
        ]
        self.difficulty = difficulty
        self.stack: ActionStack = ActionStack()
        self.step = 0

    def fill(self, row: int, col: int, num: int):
        if row == -1 or col == -1:
            return
        if self.origin_board[row, col] != 0:
            return
        self.board[row, col] = num
        action = Action(ActionType.FILL, row, col, num, self.step)
        self.stack.push(action)
        # while self.notes[row, col]:
        note = self.notes[row, col]

        self.step += 1

    def clear(self, row: int, col: int):
        self.board[row, col] = 0

    def explore(self, row: int, col: int, num: int):
        assert self.board[row, col] == 0, "Cell is already filled"
        self.board[row, col] = num
        self.row_remain_set[row].remove(num)
        self.col_remain_set[col].remove(num)
        self.block_remain_set[row // 3 * 3 + col // 3].remove(num)

    def step_back(self, row: int, col: int):
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
