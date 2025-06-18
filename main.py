import curses
from entities import Player
from renderer import Layer
from terrain import World

# Screen size
HEIGHT = 40
WIDTH = 170

# Camera bounding box
CAMERA_BOX_HEIGHT = 6
CAMERA_BOX_WIDTH = 24

# World gen constants
SEED = 12
BIOMESCALE = 256

def getCameraCords(pCords, cPos):
    pCordY, pCordX = pCords
    cPosY, cPosX = cPos

    if (pCordY - cPosY) > (CAMERA_BOX_HEIGHT // 2):
        cPosY += (pCordY - cPosY) - (CAMERA_BOX_HEIGHT // 2)
    elif (cPosY - pCordY) > (CAMERA_BOX_HEIGHT // 2):
        cPosY -= (cPosY - pCordY) - (CAMERA_BOX_HEIGHT // 2)

    if (pCordX - cPosX) > (CAMERA_BOX_WIDTH // 2):
        cPosX += (pCordX - cPosX) - (CAMERA_BOX_WIDTH // 2)
    elif (cPosX - pCordX) > (CAMERA_BOX_WIDTH // 2):
        cPosX -= (cPosX - pCordX) - (CAMERA_BOX_WIDTH // 2)

    return (cPosY, cPosX)

def getLayerCords(pCords, cPos):
    pCordY, pCordX = pCords
    cPosY, cPosX = cPos
    return (pCordY - cPosY + (HEIGHT // 2), pCordX - cPosX + (WIDTH // 2))

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
    world = World(SEED, BIOMESCALE)
    player = Player("player", "@", (11, -1), (0, 0))  # Start at world position (0, 0)

    while True:
        # Clear background layer
        bg.clear()
        # Update background position to follow player
        bg.pos = getCameraCords(player.cords, bg.pos)
        # Fill background layer with visible world tiles
        for y in range(HEIGHT):
            for x in range(WIDTH):
                posY, posX = bg.pos
                bg.data[y][x] = world.generator((posY + y, posX + x))

        # Clear foreground layer
        fg.clear()
        # Update foreground position to follow player
        fg.pos = getCameraCords(player.cords, fg.pos)
        # Draw player
        lCordY, lCordX = getLayerCords(player.cords, fg.pos)
        fg.data[lCordY][lCordX] = player

        # Render to screen
        bg.draw(stdscr)
        fg.draw(stdscr)
        stdscr.refresh()

        # Get input
        key = stdscr.getch()

        # Process input and collision
        lCordY, lCordX = getLayerCords(player.cords, fg.pos)
        player.controls(key, bg.data, (lCordY, lCordX))

        # Quit if requested
        if key == ord("q"):
            break

curses.wrapper(main)