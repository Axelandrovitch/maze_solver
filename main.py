from graphics import Window, Point, Line, Cell, Maze

def main():
    win = Window(800, 600)

    num_cols = 12
    num_rows = 10
    m1 = Maze(40, 40, num_rows, num_cols, 30, 30, win=win)
 

    win.wait_for_close()

main()
