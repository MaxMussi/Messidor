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
        
        biome = getBiome(layeredNoise)
        tile = getTile(cords, biome, self.biomeScale, self.seed)

        self.data[cords] = tile
        return tile

def getBiome(layeredNoise):
    temperature, humidity, weirdness = layeredNoise
    if -0.2 <= temperature <= 0.2 and -0.2 <= humidity <= 0.2:
        return "Plain"
    if -0.2 <= temperature <= 0.2 and 0.2 <= humidity <= 0.4:
        return "Wetland"
    elif -0.2 <= temperature <= 0.2 and -0.4 <= humidity <= -0.2:
        return "Dry plain"
    elif -0.4 <= temperature <= -0.2 and -0.4 <= humidity <= -0.2:
        return "Praire"

    #Fallback
    return "Plain"

def getTile(cords, biome, scale, seed):
    y, x = cords

    if biome == "Plain":
        gradient = random.randint(1, 100)
        
        if gradient <= 10:
            return Tile("º", (3, 22), True)
        elif gradient == 11:
            return Tile("º", (9, 22), True)
        else:
            return Tile("/", (2, 22), True)
    elif biome == "Wetland":
        terrainScale = 10
        gradient = noise.pnoise2(x / terrainScale, y / terrainScale, octaves=8, persistence=0.5, lacunarity=2.0, base=seed)
        
        if gradient > 0:
            return Tile("~", (0, 4), False)
        
        gradient = random.randint(1, 100)
        
        if gradient <= 10:
            return Tile("º", (3, 22), True)
        elif gradient == 11:
            return Tile("º", (9, 22), True)
        else:
            return Tile("/", (2, 22), True)
    elif biome == "Dry plain":
        gradient = random.randint(1, 100)
        
        if gradient <= 5:
            return Tile("º", (3, 58), True)
        elif gradient == 6:
            return Tile("º", (9, 58), True)
        else:
            return Tile("/", (100, 58), True)
    elif biome == "Praire":
        gradient = random.randint(1, 100)
        
        if gradient <= 5:
            return Tile("º", (3, 220), True)
        elif gradient == 6:
            return Tile("º", (9, 220), True)
        else:
            return Tile("/", (229, 220), True)

        
