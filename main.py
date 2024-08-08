from sudoku.generator import Generator
from sudoku.renderer import Renderer
from sudoku.level import *


def main():
    generator = Generator()
    sudoku_gt, sudoku = generator.generate(difficulty=HARD)
    # print(sudoku_gt.board)
    # print(sudoku.board)

    renderer = Renderer(sudoku)
    renderer.render()


if __name__ == "__main__":
    main()
