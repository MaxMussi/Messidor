import curses
import math
from terrain import Tile
from entities import Entity

next_color_id = 16
next_pair_id = 1

colorIDs = {}
colorPairIDs = {}

CONV = 1000 / 255

def getColor(color):
    global next_color_id
    if color in colorIDs:
        return colorIDs[color]
    if not isinstance(color, tuple) or len(color) != 3:
        raise ValueError(f"Invalid color: {color}")
    r, g, b = [int(c * CONV) for c in color]
    curses.init_color(next_color_id, r, g, b)
    colorIDs[color] = next_color_id
    next_color_id += 1
    return colorIDs[color]

def getColorPair(fgColor, bgColor):
    global next_pair_id
    key = (fgColor, bgColor)
    if key in colorPairIDs:
        return colorPairIDs[key]
    fg = getColor(fgColor)
    bg = getColor(bgColor) if bgColor else -1
    curses.init_pair(next_pair_id, fg, bg)
    colorPairIDs[key] = next_pair_id
    next_pair_id += 1
    return colorPairIDs[key]

class Layer:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.data = [[None for _ in range(width)] for _ in range(height)]
        self.frameLock = False

    def draw(self, stdscr, underlayer=None):
        self.frameLock = False
        for y in range(self.height):
            for x in range(self.width):
                tile = self.data[y][x]
                if tile is None:
                    continue

                char, color = tile.metaTile
                currentChar = char
                currentColor = color

                if getattr(tile, "frame", -1) >= 0 and getattr(tile, "simple", True):
                    if tile.frame >= max(len(char), len(color)):
                        tile.frame = 0
                    currentFrame = math.floor(tile.frame)
                    if isinstance(char, tuple):
                        currentChar = char[currentFrame]
                    if isinstance(color, tuple):
                        currentColor = color[currentFrame]
                    if self.frameLock == False:
                        tile.frame += getattr(tile, "animSpd", 1)
                        self.frameLock = True

                fgColor, bgColor = currentColor

                if bgColor is None and underlayer is not None:
                    underTile = underlayer[y][x]
                    if underTile is not None:
                        _, bg = underTile.metaTile[1]
                        if isinstance(bg[0], tuple):
                            _, bgColor = bg


                pairID = getColorPair(fgColor, bgColor)

                try:
                    stdscr.addch(y, x, currentChar, curses.color_pair(pairID))
                except curses.error:
                    pass

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.data[y][x] = None
