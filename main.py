from window import Window
from components import Point
from maze import Maze


def main():
    win = Window(800, 600)
    m1 = Maze(Point(50, 50), win=win, seed=0)
    m1.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
