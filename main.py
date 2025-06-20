import curses
import time
from renderer import Layer
from terrain import World
from entities import Player

SEED = 24
BIOMESCALE = 256

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
    return (cordY-posY+height//2, cordX-posX+width//2)

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

    world = World(SEED, BIOMESCALE)

    player = Player("Max",("@",((255,255,0), None)),(0,0),100,100,100)

    while True:
        begin = time.time()
        curses.curs_set(0)

        height, width = stdscr.getmaxyx()

        layerPos = getLayerCords(fg.pos, player.cords, height, width)

        for layer in [bg,fg,ui]:
            layer.pos = layerPos

        bg.clear(height, width)
        for y in range(height):
            for x in range(width):
                worldCord = getWorldCords(layerPos, (y, x), height, width)
                bg.data[y][x] = world.getTile(worldCord)

        fg.clear(height, width)
        cordY, cordX = getCordsInLayer(layerPos, player.cords, height, width)
        fg.data[cordY][cordX] = player
    
        bg.draw(stdscr)
        fg.draw(stdscr, bg.data)

        stdscr.refresh()

        key=stdscr.getch()

        run = player.controls(key, bg.data, fg.data, getCordsInLayer(layerPos, player.cords, height, width))

        if key == ord("q"):
            break

        if stdscr.getch() != -1:
            pass

        end = time.time()

        time.sleep(max(0, (1/24) - (end - begin)))

curses.wrapper(main)