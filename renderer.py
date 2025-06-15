import curses

class Layer:
    def __init__(self, width, height):
        self.map_data = [[" " for _ in range(width)] for _ in range(height)]
        self.map_color = [[[7, -1] for _ in range(width)] for _ in range(height)]
        self.color_cache = {}
        self.next_color_id = 1

    def draw(self, stdscr):
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                char = self.map_data[y][x]
                fg, bg = self.map_color[y][x]
                color_id = self.getColorId((fg, bg))
                if char != " ":
                    stdscr.addch(y, x, char, curses.color_pair(color_id))
                else:
                    continue
        curses.curs_set(0)

    def clear(self):
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                self.map_data[y][x] = " "
                self.map_color[y][x] = [7,-1]

    def getColorId(self, key):
        if key in self.color_cache:
            return self.color_cache[key]
        
        fg, bg = key
        curses.init_pair(self.next_color_id, fg, bg)
        self.color_cache[key] = self.next_color_id
        self.next_color_id += 1
        return self.color_cache[key]
