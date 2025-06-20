import curses
import time
from renderer import Layer
from terrain import Tile
from entities import Player

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    height, width = stdscr.getmaxyx()

    bg = Layer(height, width)
    fg = Layer(height, width)
    ui = Layer(height, width)

    floor = Tile(((".", ","),((0, 244, 0), (8, 128, 0))),animSpd=16)

    player = Player("Max",("@",((255,255,0), None)),(height//2,width//2),100,100,100)

    while True:
        begin = time.time()
        curses.curs_set(0)

        height, width = stdscr.getmaxyx()

        bg.clear(height, width)
        for y in range(height):
            for x in range(width):
                bg.data[y][x] = floor

        fg.clear(height, width)
        pCordY, pCordX = player.cords
        fg.data[pCordY][pCordX] = player
    
        bg.draw(stdscr)
        fg.draw(stdscr, bg.data)

        stdscr.refresh()

        stdscr.timeout(42)
        key=stdscr.getch()

        run = player.controls(key, bg.data, fg.data, player.cords)

        if key == ord("q"):
            break

        end = time.time()

        time.sleep(max(0, (1/24) - (end - begin)))

curses.wrapper(main)