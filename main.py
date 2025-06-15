import curses
import time
from renderer import Layer

WIDTH = 120
HEIGHT = 30

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    bg = Layer(WIDTH, HEIGHT)
    fg = Layer(WIDTH, HEIGHT)

    bg.map_data = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    bg.map_color = [[[7, 0] for _ in range(WIDTH)] for _ in range(HEIGHT)]

    playerX = WIDTH//2
    playerY = HEIGHT//2

    fg.map_data[playerY][playerX] = "@"
    fg.map_color[playerY][playerX] = [11, -1]

    while True:
        bg.draw(stdscr)
        fg.draw(stdscr)

        stdscr.refresh()
        key = stdscr.getch()

        fg.clear()

        if key == ord("w"):
            playerY -= 1
        elif key == ord("a"):
            playerX -= 1
        elif key == ord("s"):
            playerY += 1
        elif key == ord("d"):
            playerX += 1
        
        if key == ord("q"):
            break
        
        playerX = max(0, min(playerX, WIDTH - 1))
        playerY = max(0, min(playerY, HEIGHT - 1))

        fg.map_data[playerY][playerX] = "@"
        fg.map_color[playerY][playerX] = [11, -1]

curses.wrapper(main)
