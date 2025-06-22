import curses
import math

next_color_id = 1
next_pair_id = 1

colorIDs = {}
colorPairIDs = {}

CONV = 1000 / 255

def getColor(color):
    global next_color_id
    if color in colorIDs:
        return colorIDs[color]
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
        self.frame = 0
        self.pos = (0,0)

    def draw(self, stdscr, underlayer=None):
        if self.frame < 24:
            self.frame += 1
        else:
            self.frame = 0
        for y in range(self.height):
            for x in range(self.width):
                tile = self.data[y][x]
                if tile is None:
                    continue

                chars = tile.chars
                colors = tile.colors
                char = chars
                color = colors

                if isinstance(char, tuple) or (isinstance(color[0], tuple) and isinstance(color[0][0], tuple)):
                    animSpd = getattr(tile, "animSpd", 1)
                    if isinstance(chars, tuple):
                        charFrame = math.floor(self.frame / animSpd) % len(chars)
                        char = chars[charFrame]
                    if isinstance(color[0], tuple) and isinstance(color[0][0], tuple):
                        colorFrame = (self.frame // animSpd) % len(colors)
                        color = colors[colorFrame]

                fgColor, bgColor = color

                if bgColor is None and underlayer[y][x] is not None:
                    underChars = underlayer[y][x].chars
                    underColors = underlayer[y][x].colors
                    if isinstance(underColors[0][0], tuple):
                        underAnimSpd = getattr(underlayer[y][x], "animSpd", 1)
                        underFrame = (self.frame // underAnimSpd) % len(underColors)
                        underFg, underBg = underColors[underFrame]
                    else:
                        underFg, underBg = underColors
                    bgColor = underBg

                pairID = getColorPair(fgColor, bgColor)

                try:
                    stdscr.addch(y, x, char, curses.color_pair(pairID))
                except:
                    pass

    def clear(self, height, width):
        self.height = height
        self.width = width
        self.data = [[None for _ in range(width)] for _ in range(height)]

