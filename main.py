import curses
from entities import Player
from renderer import Layer
from terrain import World

# Screen size
HEIGHT = 30
WIDTH = 120

# Camera bounding box
CAMERA_BOX_HEIGHT = 6
CAMERA_BOX_WIDTH = 24

# World gen constants
SEED = 12
SCALE = 5

def main(stdscr):
    # Initialize curses colors
    curses.start_color()
    curses.use_default_colors()

    # Enable keyboard interrupt
    stdscr.nodelay(False)

    # Clear terminal
    stdscr.clear()

    # Initialize layers
    bg = Layer(WIDTH, HEIGHT, (0, 0))
    fg = Layer(WIDTH, HEIGHT, (0, 0))

    # Initialize world and player
    world = World(SEED, SCALE)
    player = Player("player", "@", (11, -1), (0, 0))  # Start at world position (0, 0)

    while True:
        # Update background position to follow player
        bg.pos = player.cords

        # Clear background layer
        bg.clear()

        # Fill background layer with visible world tiles
        for y in range(HEIGHT):
            for x in range(WIDTH):
                posY, posX = bg.pos
                bg.data[y][x] = world.generator((posY + y, posX + x))

        # Clear and draw player on foreground layer
        fg.clear()
        fg.data[HEIGHT // 2][WIDTH // 2] = player

        # Render to screen
        bg.draw(stdscr)
        fg.draw(stdscr)
        stdscr.refresh()

        # Get input
        key = stdscr.getch()

        # Process input and collision
        player.controls(key, bg.data, (HEIGHT // 2, WIDTH // 2))

        # Quit if requested
        if key == ord("q"):
            break

curses.wrapper(main)