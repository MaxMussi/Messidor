import curses

color_cache = {}
next_color_id = 1

def getColorId(key):
    global next_color_id
    if key in color_cache:
        return color_cache[key]
    
    fg, bg = key
    curses.init_pair(next_color_id, fg, bg)
    color_cache[key] = next_color_id
    next_color_id += 1
    return color_cache[key]

class Layer:
    def __init__(self, width, height):
        self.map_data = [[None for _ in range(width)] for _ in range(height)]

    def draw(self, stdscr):
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                tile = self.map_data[y][x]
                if tile is not None:
                    char = tile.char
                    fg, bg = tile.color
                    color_id = getColorId((fg, bg))
                    try:
                        stdscr.addch(y, x, char, curses.color_pair(color_id))
                    except curses.error:
                        pass
        curses.curs_set(0)

    def clear(self):
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                self.map_data[y][x] = None
