from sudoku.generator import Generator
from sudoku.renderer import Renderer
from sudoku.constants import Level


def main():
    generator = Generator()
    sudoku = generator.generate(difficulty=Level.HARD)

    renderer = Renderer(sudoku)
    renderer.render()


if __name__ == "__main__":
    main()
