from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        if not isinstance(line, Line):
            raise TypeError('Must be a Line instance')
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


class Line:
    def __init__(self, p1, p2):
        if not isinstance(p1, Point) or not isinstance(p2, Point):
            raise TypeError('Inputs must be Point instances')
        self.__p1 = p1
        self.__p2 = p2

    def draw(self, Canvas, fill_color):
        Canvas.create_line(self.__p1.get_x(), self.__p1.get_y(), self.__p2.get_x(), self.__p2.get_y(), fill=fill_color, width=2)


class Cell:
    def __init__(self, top_left, bottom_right, win, visited=False):
        if not isinstance(top_left, Point) or not isinstance(bottom_right, Point):
            raise TypeError('Inputs must be points instances')
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = Point(top_left.get_x(), bottom_right.get_y())
        self.top_right = Point(bottom_right.get_x(), top_left.get_y())
        self._win = win 
        self.visited = visited

    def draw(self):
        left_wall = Line(self.top_left, self.bottom_left)
        right_wall = Line(self.top_right, self.bottom_right)
        top_wall = Line(self.top_left, self.top_right)
        bottom_wall = Line(self.bottom_left, self.bottom_right)
        if self.has_left_wall:
            self._win.draw_line(line=left_wall, fill_color="black")
        else:
            self._win.draw_line(line=left_wall, fill_color="white")
            
        if self.has_right_wall:
            self._win.draw_line(line=right_wall, fill_color="black")
        else:
             self._win.draw_line(line=right_wall, fill_color="white")

        if self.has_top_wall:
            self._win.draw_line(line=top_wall, fill_color="black")
        else:
            self._win.draw_line(line=top_wall, fill_color="white")

        if self.has_bottom_wall:
            self._win.draw_line(line=bottom_wall, fill_color="black")
        else:
            self._win.draw_line(line=bottom_wall, fill_color="white")

    def draw_move(self, to_cell, undo=False):
        color = "red" if undo else "gray"
        center_1 = cell_center(self)
        center_2 = cell_center(to_cell)
        center_to_center = Line(center_1, center_2)
        self._win.draw_line(line=center_to_center, fill_color=color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.cells = []
        self.win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for col in range(self.num_cols):
            column = []
            for row in range(self.num_rows):
                top_left_x = self.x1 + col * self.cell_size_x
                top_left_y = self.y1 + row * self.cell_size_y
                bottom_right_x = top_left_x + self.cell_size_x
                bottom_right_y = top_left_y + self.cell_size_y

                cell = Cell(top_left=Point(x=top_left_x, y=top_left_y),
                bottom_right=Point(x=bottom_right_x, y=bottom_right_y),
                win=self.win)

                column.append(cell)
            self.cells.append(column)
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        cell = self.cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()

        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        entrance_cell = self.cells[0][0]
        exit_cell = self.cells[-1][-1]

        entrance_cell.has_left_wall = False
        self._draw_cell(i=0, j=0)
        exit_cell.has_right_wall = False
        self._draw_cell(i=-1, j=-1)

    def _break_walls_r(self, i, j):
        current_cell = self.cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []
            if i + 1 < len(self.cells) and not self.cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j + 1 < len(self.cells[0]) and not self.cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            if i - 1 >= 0 and not self.cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            if j - 1 >= 0 and not self.cells[i][j - 1].visited:
                to_visit.append((i, j - 1))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            next_cell = random.choice(to_visit)
            ni, nj = next_cell
            if ni == i + 1:
                current_cell.has_bottom_wall = False
                self.cells[ni][nj].has_top_wall = False
            elif ni == i - 1:
                current_cell.has_top_wall = False
                self.cells[ni][nj].has_bottom_wall = False
            elif nj == j + 1:
                current_cell.right_wall = False
                self.cells[ni][nj].has_left_wall = False
            elif nj == j - 1:
                current_cell.has_left_wall = False
                self.cells[ni][nj].has_right_wall = False
            self._break_walls_r(ni, nj)

    def _reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        self._solve_r(i=0, j=0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self.cells[i][j]
        current_cell.visited = True
        if current_cell is self.cells[-1][-1]:
            return True
        if (
            i > 0
            and not self.cells[i][j].has_left_wall
            and not self.cells[i - 1][j].visited
        ):
            self.cells[i][j].draw_move(self.cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i - 1][j], True)

        if (
            i < self.num_cols - 1
            and not self.cells[i][j].has_right_wall
            and not self.cells[i + 1][j].visited
        ):
            self.cells[i][j].draw_move(self.cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i + 1][j], True)

        if (
            j > 0
            and not self.cells[i][j].has_top_wall
            and not self.cells[i][j - 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j - 1], True)

        if (
            j < self.num_rows - 1
            and not self.cells[i][j].has_bottom_wall
            and not self.cells[i][j + 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j + 1], True)

        return False


#helper functions


def cell_center(cell: Cell) -> Point:
    x1 = cell.bottom_right.get_x()
    x2 = cell.top_left.get_x()
    y1 = cell.bottom_right.get_y()
    y2 = cell.top_left.get_y()
    x = max(x1, x2) - (abs(x1 - x2)/2)
    y = max(y1, y2) - (abs(y1 - y2)/2)
    return Point(x, y)

