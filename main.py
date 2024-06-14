from graphics import Window, Point, Line

def main():
    win = Window(800, 600)

    point1 = Point(40, 70)
    point2 = Point(200, 400)
    line1 = Line(point1, point2)
    win.draw_line(line=line1, fill_color="blue")

    win.wait_for_close()

main()
