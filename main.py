import curses
from entities import Player, Creature
from entities import Spawner
from renderer import Layer
from terrain import World

# Screen dimensions
HEIGHT = 40
WIDTH = 170

# Camera bounding box size
CAMERA_BOX_HEIGHT = 6
CAMERA_BOX_WIDTH = 24

# World generation constants
SEED = 12
BIOMESCALE = 256

def getCameraCords(pCords, cPos):
    pY, pX = pCords
    cY, cX = cPos

    if (pY - cY) > (CAMERA_BOX_HEIGHT // 2):
        cY += (pY - cY) - (CAMERA_BOX_HEIGHT // 2)
    elif (cY - pY) > (CAMERA_BOX_HEIGHT // 2):
        cY -= (cY - pY) - (CAMERA_BOX_HEIGHT // 2)

    if (pX - cX) > (CAMERA_BOX_WIDTH // 2):
        cX += (pX - cX) - (CAMERA_BOX_WIDTH // 2)
    elif (cX - pX) > (CAMERA_BOX_WIDTH // 2):
        cX -= (cX - pX) - (CAMERA_BOX_WIDTH // 2)

    return (cY, cX)

def getLayerCords(pCords, cPos):
    pY, pX = pCords
    cY, cX = cPos
    return (pY - cY + (HEIGHT // 2), pX - cX + (WIDTH // 2))

def main(stdscr):
    # Initialize curses color system
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(False)
    stdscr.clear()

    # Create background and foreground layers
    bg = Layer(WIDTH, HEIGHT, (0, 0))
    fg = Layer(WIDTH, HEIGHT, (0, 0))

    # Initialize world, player and spawner
    world = World(SEED, BIOMESCALE)
    player = Player("player", "@", (11, -1), (0, 0), 100, 100, 100)
    spawner = Spawner(10, 0)

    while True:
        # Update camera position
        camera_pos = getCameraCords(player.cords, fg.pos)
        bg.pos = camera_pos
        fg.pos = camera_pos

        # Fill background layer with world tiles
        bg.clear()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                posY, posX = bg.pos
                bg.data[y][x] = world.generator((posY + y, posX + x))

        # Fill foreground layer with entities
        fg.clear()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                posY, posX = fg.pos
                world_coords = (posY + y, posX + x)
                entity = spawner.getMob(world_coords, world)
                if entity:
                    fg.data[y][x] = entity

        # Run AI for all visible creatures
        for y in range(HEIGHT):
            for x in range(WIDTH):
                creature = fg.data[y][x]
                if creature and not isinstance(creature, Player):
                    old_cords = creature.cords
                    creature.tickAi(bg.data, fg.data)
                    if creature.cords != old_cords:
                        fg.data[y][x] = None
                        lY, lX = getLayerCords(creature.cords, fg.pos)
                        if 0 <= lY < HEIGHT and 0 <= lX < WIDTH:
                            fg.data[lY][lX] = creature

        # Draw the player
        lY, lX = getLayerCords(player.cords, fg.pos)
        if 0 <= lY < HEIGHT and 0 <= lX < WIDTH:
            fg.data[lY][lX] = player

        # Render both layers
        bg.draw(stdscr)
        fg.draw(stdscr)
        stdscr.refresh()

        # Handle input
        key = stdscr.getch()

        # Move player
        lY, lX = getLayerCords(player.cords, fg.pos)
        player.controls(key, bg.data, fg.data, (lY, lX))

        # Exit on 'q'
        if key == ord("q"):
            break

curses.wrapper(main)
