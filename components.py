class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)


class Cell():
    def __init__(self, center, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.center = center
        self.visited = False

        self.__win = window

    def draw(self, size):
        if not self.__win:
            return
        half_size = size // 2
        if self.has_left_wall:
            line = Line(Point(self.center.x - half_size, self.center.y - half_size), Point(self.center.x - half_size, self.center.y + half_size))
            self.__win.draw_line(line)
        if self.has_right_wall:
            line = Line(Point(self.center.x + half_size, self.center.y - half_size), Point(self.center.x + half_size, self.center.y + half_size))
            self.__win.draw_line(line)
        if self.has_top_wall:
            line = Line(Point(self.center.x - half_size, self.center.y - half_size), Point(self.center.x + half_size, self.center.y - half_size))
            self.__win.draw_line(line)
        if self.has_bottom_wall:
            line = Line(Point(self.center.x - half_size, self.center.y + half_size), Point(self.center.x + half_size, self.center.y + half_size))
            self.__win.draw_line(line)

    def draw_move(self, to_cell, undo=False):
        line_color = "gray" if undo else "red"
        line = Line(self.center, to_cell.center)
        line.draw(self.__win.canvas, line_color)
