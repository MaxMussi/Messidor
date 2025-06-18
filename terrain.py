import noise
import random
from tiles import Tile

class World:
    def __init__(self, seed, biomeScale):
        random.seed(seed)
        self.seed = seed
        self.biomeScale = biomeScale
        self.data = {}
    
    def generator(self, cords):
        y, x = cords

        if cords in self.data:
            return self.data[cords]

        temperature = noise.pnoise2(x / self.biomeScale, y / self.biomeScale, octaves=3, base=self.seed + 1)
        humidity = noise.pnoise2(x / self.biomeScale, y / self.biomeScale, octaves=3, base=self.seed + 2)
        weirdness = noise.pnoise2(x / self.biomeScale, y / self.biomeScale, octaves=3, base=self.seed + 3)
        layeredNoise = (temperature, humidity, weirdness)
        
        biome = self.getBiome(layeredNoise)
        self.generateTile(cords, biome)

        return self.data[cords]

    def getBiome(self, layeredNoise):
        temperature, humidity, weirdness = layeredNoise
        #Fallback
        return "Forest"

    def generateTile(self, cords, biome):

        if biome == "Forest":
            gradient = random.randint(1, 2400)
            if gradient <= 60:
                self.data[cords] = Tile("º", (3, 22), True)
            elif gradient <= 120:
                self.data[cords] = Tile("*", (2, 22), True)
            elif gradient <= 125:
                self.data[cords] = Tile("º", (9, 22), True)
            elif gradient == 126:
                self.spawnFeature(cords, "Tree stump")
            else:
                self.data[cords] = Tile("/", (2, 22), True)
    
    def spawnFeature(self, cords, feature):
        y, x = cords

        if feature == "Tree stump":
            gradient = random.randint(0, 1)
            if gradient == 0:
                self.data[(y, x)] = Tile("|", (130, 94), False)
                self.data[(y + 1, x)] = Tile("|", (130, 94), False)
                self.data[(y + 2, x)] = Tile("|", (130, 94), False)
                self.data[(y + 3, x)] = Tile("|", (130, 94), False)
            else:
                self.data[(y, x)] = Tile("-", (130, 94), False)
                self.data[(y, x + 1)] = Tile("-", (130, 94), False)
                self.data[(y, x + 2)] = Tile("-", (130, 94), False)
                self.data[(y, x + 3)] = Tile("-", (130, 94), False)

        

        
