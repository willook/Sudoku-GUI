import pygame

from sudoku.entity import Sudoku


class Renderer:
    def __init__(self, sudoku: Sudoku):
        self.cell_size = 60
        self.cell_row_offset = 20
        self.cell_col_offset = 20
        self.sudoku = sudoku
        self.init_screen()
        self.cursors = [-1, -1]

    def init_screen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Sudoku")
        self.screen.fill((255, 255, 255))
        self.draw_num_pad()
        self.draw_board()

    def render(self):
        """
        Render the given Sudoku puzzle.
        """
        running = True
        while running:
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                # click cell
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.screen.fill((255, 255, 255))
                    i, j = self.pos_to_cell(*pygame.mouse.get_pos())
                    self.cursors = [i, j]
                    self.highlight_cell(i, j)
                # q to quit
                if key[pygame.K_q] or key[pygame.K_ESCAPE]:
                    running = False

            self.draw_num_pad()
            self.draw_board()
            # clock.tick(60)
            pygame.display.flip()
            # print("rendering")
        pygame.quit()

    def highlight_cell(self, i, j):
        """
        Highlight the cell at (i, j).
        """
        adj_color = (235, 235, 255)
        cell_color = (215, 215, 255)
        if i == -1:
            return
        cell_size = self.cell_size
        cell_row_offset = self.cell_row_offset
        cell_col_offset = self.cell_col_offset
        # row highlight
        pygame.draw.rect(
            self.screen,
            adj_color,
            (
                cell_row_offset,
                i * cell_size + cell_col_offset,
                cell_size * 9,
                cell_size,
            ),
        )
        # col highlight
        pygame.draw.rect(
            self.screen,
            adj_color,
            (
                j * cell_size + cell_row_offset,
                cell_col_offset,
                cell_size,
                cell_size * 9,
            ),
        )
        # block highlight
        r, c = i // 3 * 3, j // 3 * 3
        pygame.draw.rect(
            self.screen,
            adj_color,
            (
                c * cell_size + cell_row_offset,
                r * cell_size + cell_col_offset,
                cell_size * 3,
                cell_size * 3,
            ),
        )
        # cell highlight
        pygame.draw.rect(
            self.screen,
            cell_color,
            (
                j * cell_size + cell_row_offset,
                i * cell_size + cell_col_offset,
                cell_size,
                cell_size,
            ),
        )

    def pos_to_cell(self, x, y):
        """
        Convert the mouse position to cell indices.
        """
        if x < self.cell_col_offset or x > 9 * self.cell_size + self.cell_col_offset:
            return -1, -1
        i = (y - self.cell_row_offset) // self.cell_size
        j = (x - self.cell_col_offset) // self.cell_size
        return i, j

    def draw_num_pad(self):
        """
        Draw the number pad.
        """
        font = pygame.font.Font(None, 50)

        i0, j0 = 600, 20
        hop = 100
        for i in range(3):
            for j in range(3):
                i_offset, j_offset = 0, 0
                pygame.draw.rect(
                    self.screen,
                    (235, 235, 255),
                    (
                        i0 + i_offset + i * hop,
                        j0 + j_offset + j * hop,
                        hop - 5,
                        hop - 5,
                    ),
                )
                text = font.render(str(i * 3 + j), True, (100, 100, 255))
                i_offset, j_offset = 38, 33
                self.screen.blit(
                    text, (i0 + i_offset + i * hop, j0 + j_offset + j * hop)
                )

    def draw_board(self):
        """
        Draw the Sudoku board.
        """
        font = pygame.font.Font(None, 40)
        cell_size = self.cell_size
        cell_row_offset = self.cell_row_offset
        cell_col_offset = self.cell_col_offset
        for i in range(9):
            for j in range(9):
                num = self.sudoku.board[i, j]
                if num != 0:
                    text = font.render(str(num), False, (0, 0, 0))
                    self.screen.blit(text, (j * cell_size + 45, i * cell_size + 40))
        for i in [1, 2, 4, 5, 7, 8, 0, 3, 6, 9]:
            color = (0, 0, 0) if i % 3 == 0 else (200, 200, 200)
            pygame.draw.line(
                self.screen,
                color,
                (cell_row_offset, i * cell_size + cell_col_offset),
                (cell_row_offset + 9 * cell_size, i * cell_size + cell_col_offset),
                2,
            )
            pygame.draw.line(
                self.screen,
                color,
                (i * cell_size + cell_row_offset, cell_col_offset),
                (i * cell_size + cell_row_offset, 9 * cell_size + cell_col_offset),
                2,
            )
