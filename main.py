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
        cordY - posY + height // 2,
        cordX - posX + width // 2
    )

def fillBg(bg, world, layerPos, height, width):
    for y in range(height):
            for x in range(width):
                worldCord = getWorldCords(layerPos, (y, x), height, width)
                bg.data[y][x] = world.getTile(worldCord)

def playerControls(player, mapData, entityData, stdscr):
    key = stdscr.getch()
    run = player.controls(key, mapData, entityData, player.cords)
    if stdscr.getch() == -1:
        pass
    if key == ord("q"):
        return None
    else:
        return run

def tickAi(spawnerData, worldData, layerPos, height, width):
    creatures = []
    for y in range(height):
        for x in range(width):
            wCords = getWorldCords(layerPos, (y, x), height, width)
            if isinstance(spawnerData.get(wCords, None), Creature):
                creatures.append(spawnerData.get(wCords, None))

    for entity in creatures:
        oldY, oldX = entity.cords
        entity.tickAi(worldData, spawnerData)
        newY, newX = entity.cords
        if (newY, newX) != (oldY, oldX):
            spawnerData.pop((oldY, oldX), None)
            spawnerData[(newY, newX)] = entity

def spawn(spawner, fgData, layerPos, height, width):
    for y in range(height):
        for x in range(width):
            entity = spawner.attemptSpawn(getWorldCords(layerPos, (y,x), height, width))
            fgData[y][x] = entity
    return fgData


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

    fg.data = spawn(spawner, fg.data, fg.pos, height, width)

    while True:
        begin = time.time()
        curses.curs_set(0)

        height, width = stdscr.getmaxyx()

        run = playerControls(player, world.data, spawner.data, stdscr)

        if run:
            layerPos = getLayerCords(fg.pos, player.cords, height, width)
            bg.pos = layerPos
            fg.pos = layerPos

            tickAi(spawner.data, world.data, fg.pos, height, width)
            fg.data = spawn(spawner, fg.data, fg.pos, height, width)
        elif run is None:
            break
        
        scrY, scrX = getCordsInLayer(fg.pos, player.cords, height, width)
        fg.data[scrY][scrX] = player

        bg.clear(height, width)
        fillBg(bg, world, bg.pos, height, width)

        bg.draw(stdscr)
        fg.draw(stdscr, bg.data)

        stdscr.addstr(0, 0, f"Player cords: {player.cords}")
        stdscr.addstr(1, 0, f"Layer cords: {fg.pos}")
        stdscr.addstr(2, 0, f"Player cords in layer: {(scrY, scrX)}")
        stdscr.refresh()

        end = time.time()
        time.sleep(max(0, (1 / 24) - (end - begin)))

curses.wrapper(main)
