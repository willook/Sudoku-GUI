from typing import Union

import numpy as np

from sudoku.entity import Sudoku
from sudoku.solver import BacktrackingSolver
from sudoku.constants import Level


class Generator:
    def __init__(self, max_iter: int = 1_000):
        self.max_iter = max_iter

    def generate(self, difficulty: int = 1) -> tuple[Sudoku, Sudoku]:
        """
        Generate a Sudoku puzzle with a given difficulty level.
        The difficulty level is an integer between 1 and 5.
        1 is the easiest, 5 is the hardest.
        """
        assert 1 <= difficulty <= 5, "Difficulty level must be between 1 and 5"
        full_sudoku = self._generate_random_full_sudoku()
        sudoku = self._remove_numbers(full_sudoku, difficulty)
        sudoku.board_gt = full_sudoku.board
        return sudoku

    def _remove_numbers(self, sudoku: Sudoku, difficulty: int):
        """
        Remove numbers from the board to create a Sudoku puzzle.
        """
        board = sudoku.board.copy()
        n = 81
        if difficulty == Level.EASY:
            n = 30
        elif difficulty == Level.NORMAL:
            n = 35
        elif difficulty == Level.HARD:
            n = 40
        elif difficulty == Level.MASTER:
            n = 45
        elif difficulty == Level.EXTREME:
            n = 50
        indices = np.random.choice(81, n, replace=False)
        for idx in indices:
            board[idx // 9, idx % 9] = 0
        return Sudoku(board)

    def _generate_random_full_sudoku(self) -> Sudoku:
        """
        Generate a random full Sudoku board.
        """
        while True:
            try:
                board = np.zeros((9, 9), dtype=int)
                for i in range(0, 9, 3):
                    self._fill_diagonal(board, i, i)
                sudoku = Sudoku(board)
                solver = BacktrackingSolver(self.max_iter)
                ret = solver.solve(sudoku)
                assert ret, "Failed to generate a random full board"
                break
            except TimeoutError:
                pass
        return sudoku

    def _fill_diagonal(self, board: np.ndarray, row, col):
        """
        Fill the diagonal of the board with random numbers.
        """
        nums = np.random.permutation(9) + 1
        for k in range(9):
            board[row + k // 3, col + k % 3] = nums[k]
