import curses
import time
from renderer import Layer
from terrain import World
from entities import Player, Spawner, Creature

SEED = 24
BIOMESCALE = 256
NOISE = 64

def getWorldCords(pos, cords, height, width):
    posY, posX = pos
    cordY, cordX = cords
    worldY = posY + cordY - height // 2
    worldX = posX + cordX - width // 2
    return (worldY, worldX)

def getLayerCords(currentPos, playerPos, height, width):
    posY, posX = currentPos
    plyY, plyX = playerPos
    boxHeight = height // 4
    boxWidth = width // 4

    if (plyY - posY) > (boxHeight // 2):
        posY += (plyY - posY) - (boxHeight // 2)
    elif (posY - plyY) > (boxHeight // 2):
        posY -= (posY - plyY) - (boxHeight // 2)

    if (plyX - posX) > (boxWidth // 2):
        posX += (plyX - posX) - (boxWidth // 2)
    elif (posX - plyX) > (boxWidth // 2):
        posX -= (posX - plyX) - (boxWidth // 2)

    return (posY, posX)

def getCordsInLayer(pos, cords, height, width):
    posY, posX = pos
    cordY, cordX = cords
    return (
        cordY - posY + (height - 1) // 2,
        cordX - posX + (width - 1) // 2
    )

def in_bounds(data, y, x):
    return 0 <= y < len(data) and 0 <= x < len(data[0])

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

    world = World(SEED, BIOMESCALE, NOISE)
    player = Player("@", ((255, 255, 0), None), (0, 0), "Max", 100, 100, 100)
    spawner = Spawner(1, world)

    while True:
        begin = time.time()
        curses.curs_set(0)
        height, width = stdscr.getmaxyx()
        layerPos = getLayerCords(fg.pos, player.cords, height, width)

        for layer in [bg, fg, ui]:
            layer.pos = layerPos

        bg.clear(height, width)
        fg.clear(height, width)

        for y in range(height):
            for x in range(width):
                worldCord = getWorldCords(layerPos, (y, x), height, width)
                bg.data[y][x] = world.getTile(worldCord)

        key = stdscr.getch()
        run = player.controls(key, bg.data, fg.data, getCordsInLayer(layerPos, player.cords, height, width))
        if key == ord("q"):
            break
        if stdscr.getch() == -1:
            pass

        if run:
            creatures = []
            for y in range(height):
                for x in range(width):
                    worldCord = getWorldCords(layerPos, (y, x), height, width)
                    entity = spawner.data.get(worldCord)
                    if isinstance(entity, Creature):
                        creatures.append(entity)

            for entity in creatures:
                oldY, oldX = getCordsInLayer(layerPos, entity.cords, height, width)
                entity.tickAi(bg.data, fg.data, (oldY, oldX))
                newY, newX = getCordsInLayer(layerPos, entity.cords, height, width)
                if (newY, newX) != (oldY, oldX):
                    oldWorld = getWorldCords(layerPos, (oldY, oldX), height, width)
                    newWorld = entity.cords
                    spawner.data.pop(oldWorld, None)
                    spawner.data[newWorld] = entity

        for y in range(height):
            for x in range(width):
                worldCord = getWorldCords(layerPos, (y, x), height, width)
                entity = spawner.data.get(worldCord)
                if not entity:
                    entity = spawner.attemptSpawn(worldCord)
                if entity:
                    fg.data[y][x] = entity

        cordY, cordX = getCordsInLayer(layerPos, player.cords, height, width)
        if in_bounds(fg.data, cordY, cordX):
            fg.data[cordY][cordX] = player

        bg.draw(stdscr)
        fg.draw(stdscr, bg.data)

        stdscr.addstr(0, 0, f"Player cords: {player.cords}")
        stdscr.addstr(1, 0, f"Layer cords: {layerPos}")
        stdscr.addstr(2, 0, f"Player cords in layer: {(cordY, cordX)}")
        stdscr.refresh()

        end = time.time()
        time.sleep(max(0, (1 / 24) - (end - begin)))

curses.wrapper(main)
