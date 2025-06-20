import random
import noise

class Tile:
    def __init__(self, metaTile, passable=True, animSpd=0):
        self.metaTile = metaTile
        self.passable = passable
        self.animSpd = animSpd

class World:
    def __init__(self, seed, biomeScale):
        random.seed(seed)
        self.seed = seed
        self.biomeScale = biomeScale
        self.data = {}

    def getTile(self, cords):
        if cords in self.data:
            return self.data[cords]

        layeredNoise = self.getLayeredNoise(cords)
        biome = self.getBiome(layeredNoise)
        tile = biome.generate(cords)
        self.data[cords] = tile
        return tile

    def getLayeredNoise(self, cords):
        y, x = cords
        temp = noise.pnoise2(x / self.biomeScale, y / self.biomeScale, octaves=3, base=self.seed + 1)
        hum = noise.pnoise2(x / self.biomeScale, y / self.biomeScale, octaves=3, base=self.seed + 2)
        weird = min(noise.pnoise2(x / self.biomeScale, y / self.biomeScale, octaves=3, base=self.seed + 3),0)
        return (temp, hum, weird)

    def getBiome(self, layeredNoise):
        temp, hum, weird = layeredNoise
        return Forest()

class Biome:
    def __init__(self, temp, hum, weird):
        self.temp = temp
        self.hum = hum
        self.weird = weird

    def generate(self, cords):
        raise NotImplementedError

class Forest(Biome):
    def __init__(self):
        self.temp = 0
        self.hum = 0.2
        self.weird = 0
    def generate(self, cords):
        roll = random.randint(0,1)
        if roll == 0:
            return Tile((".", ((255, 255, 255),(0,0,0))), passable=True)
        return Tile((",", ((255, 255, 255),(0,0,0))), passable=True)
