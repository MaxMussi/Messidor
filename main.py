import curses
import time
from renderer import Layer
from terrain import Tile
from entities import Player

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)

    height, width = stdscr.getmaxyx()

    bg = Layer(height, width)
    fg = Layer(height, width)
    ui = Layer(height, width)

    floor = Tile(((".", ","),((255, 255, 255), (0, 0, 0))),animSpd=8)

    player = Player("Max",("@",((255,255,0), None)),(height//2,width//2),100,100,100)

    while True:
        curses.curs_set(0)

        height, width = stdscr.getmaxyx()
        for layer in [bg, fg, ui]:
            layer.height = height
            layer.width = width

        bg.clear()
        for y in range(height):
            for x in range(width):
                bg.data[y][x] = floor

        fg.clear()
        pCordY, pCordX = player.cords
        fg.data[pCordY][pCordX] = player
    
        bg.draw(stdscr)
        fg.draw(stdscr, bg.data)

        stdscr.refresh()

        stdscr.timeout(17)
        key=stdscr.getch()

        run = player.controls(key, bg.data, fg.data, player.cords)

        if key == ord("q"):
            break

        time.sleep(1/60)

curses.wrapper(main)