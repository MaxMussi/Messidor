import curses
import noise
from tiles import Tile
from entities import Player
from renderer import Layer

WIDTH = 120
HEIGHT = 30

COBBLE_SCALE = 5
THRESHOLD = 0.15

SEED = 24

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    bg = Layer(WIDTH, HEIGHT)
    fg = Layer(WIDTH, HEIGHT)

    floor = Tile(".", (15, -1), True)
    cobble = Tile("#", (8, -1), False)

    bg.map_data = [[floor for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            val = noise.pnoise2(x / COBBLE_SCALE, y / COBBLE_SCALE, octaves=3, persistence=0.5, base=SEED)
            if val > THRESHOLD:
                bg.map_data[y][x] = cobble
            else:
                bg.map_data[y][x] = floor

    player = Player("player", (11, -1), HEIGHT//2, WIDTH//2)

    fg.map_data[player.cordY][player.cordX] = player

    while True:
        bg.draw(stdscr)
        fg.draw(stdscr)

        stdscr.refresh()
        key = stdscr.getch()

        fg.clear()

        player.controls(key, bg.map_data)
        
        if key == ord("q"):
            break

        fg.map_data[player.cordY][player.cordX] = player

curses.wrapper(main)
