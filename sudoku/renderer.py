import pygame

from sudoku.entity import Sudoku


class Renderer:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.cell_size = 60
        self.cell_row_offset = 20
        self.cell_col_offset = 20
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
            # check there is any event, if not, skip the loop
            event_list = pygame.event.get()
            key = pygame.key.get_pressed()
            if not event_list and not any(key):
                pygame.time.wait(50)
                continue
            else:
                self.screen.fill((255, 255, 255))

            for event in event_list:
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    i, j = self.pos_to_cell(*pygame.mouse.get_pos())
                    self.cursors = [i, j]
                # key down
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        num = int(event.unicode)
                        self.sudoku.fill(self.cursors[0], self.cursors[1], num)
                    elif event.key == pygame.K_BACKSPACE:
                        self.sudoku.fill(self.cursors[0], self.cursors[1], 0)
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False

            self.highlight_cell()
            self.draw_num_pad()
            self.draw_board()
            # clock.tick(60)
            pygame.display.flip()
            # print("rendering")
        pygame.quit()

    def highlight_cell(self):
        """
        Highlight the cell at (i, j).
        """
        i, j = self.cursors
        if i == -1 or j == -1:
            return
        adj_color = (235, 235, 255)
        cell_color = (215, 215, 255)
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
                text = font.render(str(i + j * 3 + 1), True, (100, 100, 255))
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
        base_num_color = (0, 0, 0)
        right_num_color = (0, 0, 200)
        wrong_num_color = (200, 0, 0)
        for i in range(9):
            for j in range(9):
                num = self.sudoku.board[i, j]
                if num == 0:
                    continue
                if self.sudoku.origin_board[i, j] != 0:
                    text = font.render(str(num), False, base_num_color)
                elif self.sudoku.board_gt[i, j] == num:
                    text = font.render(str(num), False, right_num_color)
                else:
                    text = font.render(str(num), False, wrong_num_color)
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
