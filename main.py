import curses
from tiles import Tile
from entities import Player
from renderer import Layer

WIDTH = 120
HEIGHT = 30

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    bg = Layer(WIDTH, HEIGHT)
    fg = Layer(WIDTH, HEIGHT)

    floor = Tile(".", (15, -1), True)

    bg.map_data = [[floor for _ in range(WIDTH)] for _ in range(HEIGHT)]

    player = Player("player", (11, -1), HEIGHT//2, WIDTH//2)

    fg.map_data[player.cordY][player.cordX] = player

    while True:
        bg.draw(stdscr)
        fg.draw(stdscr)

        stdscr.refresh()
        key = stdscr.getch()

        fg.clear()

        player.controls(key)
        
        if key == ord("q"):
            break

        fg.map_data[player.cordY][player.cordX] = player

curses.wrapper(main)
