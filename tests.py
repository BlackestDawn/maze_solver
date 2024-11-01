import unittest
from components import Maze, Point


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), num_cols, num_rows, 10, None, 0)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_resetting_visited_cells(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(Point(0, 0), num_cols, num_rows, 10, None, 0)
        for column in m1._cells:
            for cell in column:
                self.assertEqual(cell.visited, False)


if __name__ == "__main__":
    unittest.main()
