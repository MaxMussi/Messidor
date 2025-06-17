import noise
from tiles import Tile

class World:
    def __init__(self, seed, scale):
        self.seed = seed
        self.scale = scale
        self.data = {}
    
    def generator(self, cords):
        y, x = cords

        if cords in self.data:
            gradient = self.data[cords]
        else:
            gradient = noise.pnoise2(x / self.scale, y / self.scale, octaves=3, persistence=0.5, lacunarity=2.0, base=self.seed)
            self.data[cords] = gradient

        if gradient > 0.15:
            return Tile("#", (8,-1), False)
        else:
            return Tile(".", (7,-1), True)