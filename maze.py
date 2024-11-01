import random
from time import sleep
from components import Point, Cell


class Maze():
    def __init__(self, anchor, num_cols=None, num_rows=None, cell_size=50, win=None, seed=None):
        self.anchor_point = anchor
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size = cell_size
        self.__win = win

        if seed is not None:
            random.seed(seed)

        if self.num_cols is None:
            width = 800 if self.__win is None else self.__win.width
            margine = abs(self.anchor_point.x - self.cell_size // 2)
            self.num_cols = (width - 2 * margine) // self.cell_size

        if self.num_rows is None:
            height = 600 if self.__win is None else self.__win.height
            margine = abs(self.anchor_point.y - self.cell_size // 2)
            self.num_rows = (height - 2 * margine) // self.cell_size

        self._create_cells()
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            cell_column = []
            for j in range(self.num_rows):
                x = self.anchor_point.x + (self.cell_size * i)
                y = self.anchor_point.x + (self.cell_size * j)
                cell_center = Point(x, y)
                cell_column.append(Cell(cell_center, self.__win))
            self._cells.append(cell_column)

        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

        if self.__win:
            self._draw_cells()

    def _draw_cells(self):
        if not self.__win:
            self._draw_cells()
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].draw(self.cell_size)
                self._animate()

    def _animate(self):
        if not self.__win:
            return
        self.__win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall = False

    def _break_walls_r(self, i, j):
        if self._cells[i][j].visited:
            return
        self._cells[i][j].visited = True
        to_visit = []

        # left cell
        if i - 1 >= 0 and not self._cells[i - 1][j].visited:
            to_visit.append((i - 1, j,))
        # right cell
        if i + 1 < self.num_cols and not self._cells[i + 1][j].visited:
            to_visit.append((i + 1, j,))
        # top cell
        if j - 1 >= 0 and not self._cells[i][j - 1].visited:
            to_visit.append((i, j - 1,))
        # bottom cell
        if j + 1 < self.num_rows and not self._cells[i][j + 1].visited:
            to_visit.append((i, j + 1,))

        while len(to_visit) > 0:
            move_to = random.randrange(0, len(to_visit))
            x, y = to_visit.pop(move_to)
            if self._cells[x][y].visited:
                continue
            if i > x:
                self._cells[i][j].has_left_wall = False
                self._cells[x][y].has_right_wall = False
            elif i < x:
                self._cells[i][j].has_right_wall = False
                self._cells[x][y].has_left_wall = False
            elif j > y:
                self._cells[i][j].has_top_wall = False
                self._cells[x][y].has_bottom_wall = False
            elif j < y:
                self._cells[i][j].has_bottom_wall = False
                self._cells[x][y].has_top_wall = False
            self._break_walls_r(x, y)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # Checking left
        x = i - 1
        y = j
        if not self._cells[i][j].has_left_wall and x >= 0 and not self._cells[x][y].visited:
            from_cell = self._cells[i][j]
            to_cell = self._cells[x][y]
            from_cell.draw_move(to_cell)
            success = self._solve_r(x, y)
            if success:
                return success
            from_cell.draw_move(to_cell, True)
        # Checking right
        x = i + 1
        y = j
        if not self._cells[i][j].has_right_wall and x < self.num_cols and not self._cells[i + 1][j].visited:
            from_cell = self._cells[i][j]
            to_cell = self._cells[x][y]
            from_cell.draw_move(to_cell)
            success = self._solve_r(x, y)
            if success:
                return success
            from_cell.draw_move(to_cell, True)
        # Checking top
        x = i
        y = j - 1
        if not self._cells[i][j].has_top_wall and y >= 0 and not self._cells[i][j - 1].visited:
            from_cell = self._cells[i][j]
            to_cell = self._cells[x][y]
            from_cell.draw_move(to_cell)
            success = self._solve_r(x, y)
            if success:
                return success
            from_cell.draw_move(to_cell, True)
        # Checking bottom
        x = i
        y = j + 1
        if not self._cells[i][j].has_bottom_wall and y < self.num_rows and not self._cells[i][j + 1].visited:
            from_cell = self._cells[i][j]
            to_cell = self._cells[x][y]
            from_cell.draw_move(to_cell)
            success = self._solve_r(x, y)
            if success:
                return success
            from_cell.draw_move(to_cell, True)

        return False
