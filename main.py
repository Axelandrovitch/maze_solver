from graphics import Window, Point, Line, Cell

def main():
    win = Window(800, 600)

    point1 = Point(40, 70)
    point2 = Point(200, 400)

    cell1 = Cell(point1, point2, win)
    cell1.has_left_wall = False
    cell1.draw()

    # Additional test cells
    point3 = Point(210, 70)
    point4 = Point(370, 400)

    cell2 = Cell(point3, point4, win)
    cell2.has_right_wall = False
    cell2.has_bottom_wall = False
    cell2.draw()

    cell1.draw_move(to_cell=cell2)

    win.wait_for_close()

main()
