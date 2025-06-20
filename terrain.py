class Tile:
    def __init__(self, metaTile, passable=True, frame=-1, simple=True, animSpd = 0):
        self.metaTile = metaTile
        self.passable = passable
        self.frame = frame
        self.simple = simple
        self.animSpd = animSpd