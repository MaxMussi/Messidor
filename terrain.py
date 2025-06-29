import random
import noise

class Tile:
    def __init__(self, chars, colors, passable=True, animSpd=0):
        self.chars = chars
        self.colors = colors
        self.passable = passable
        self.animSpd = animSpd

class World:
    def __init__(self, seed, biomeScale, noise):
        random.seed(seed)
        self.seed = seed
        self.biomeScale = biomeScale
        self.noise = noise
        self.data = {}

    def getTile(self, cords):
        if cords in self.data:
            return self.data[cords]

        layeredNoise = self.getLayeredNoise(cords)
        biome = self.getBiome(layeredNoise)
        tile = biome.generate(cords, self.seed)

        self.data[cords] = tile
        return tile

    def getLayeredNoise(self, cords):
        y, x = cords
        temp = noise.pnoise2(y / self.biomeScale, x / self.biomeScale, octaves=4, persistence=1/4, base=self.seed + 1)
        hum = noise.pnoise2(y / self.biomeScale, x / self.biomeScale, octaves=4, persistence=1/4, base=self.seed + 2)
        weird = max(noise.pnoise2(y / self.biomeScale, x / self.biomeScale, octaves=4, persistence=1/4, base=self.seed + 3),0)
        return (temp, hum, weird)

    def getBiome(self, layeredNoise):
        temp, hum, weird = layeredNoise
        jitter = lambda: (random.random() - 0.5) * 2 / self.noise
        temp += jitter()
        hum += jitter()
        weird += random.random() / self.noise
        if -1 <= temp < -1/8:
            if -1 <= hum < -1/8:
                return Forest()
            elif -1/8 <= hum < 1/8:
                return Forest()
            elif 1/8 <= hum <= 1:
                return Forest()
        elif -1/8 <= temp <= 1/8:
            if -1 <= hum < -1/8:
                return DryPlains()
            elif -1/8 <= hum < 1/8:
                return Plains()
            elif 1/8 <= hum <= 1:
                return WetPlains()
        elif -1/8 <= temp <= 1:
            if -1 <= hum < -1/8:
                return Forest()
            elif -1/8 <= hum < 1/8:
                return Forest()
            elif 1/8 <= hum <= 1:
                return Forest()
        return Plains()

class Biome:
    def __init__(self):
        pass
    def generate(self, cords, seed):
        y, x = cords
        random.seed(str((y, x, seed)))

class Plains(Biome):
    def __init__(self):
        self.GRASS_LIGHTER = (64, 156, 11)
        self.GRASS_LIGHT = (60, 147, 10)
        self.GRASS_TALL = (48, 84, 27)
        self.FLOWER_YELLOW = (240, 236, 17)
        self.FLOWER_RED = (178, 49, 10)
        self.FLOWER_BLUE = (10, 24, 148)
        self.FLOWER_PURPLE = (62, 25, 63)
    def generate(self, cords, seed):
        y, x = cords
        random.seed(str((y, x, seed)))
        gradient = noise.pnoise2(y / 12, x / 12, octaves=4, persistence=1,base=seed)
        if gradient >= 0:
            bg = self.GRASS_LIGHT
        else:
            bg = self.GRASS_LIGHTER
        roll = random.randint(1,8)
        if roll == 1:
            roll = random.randint(1,48)
            if roll <= 24:
                tile = Tile(("º","o"),((self.FLOWER_YELLOW),(bg)),True,16)
            elif roll <= 38:
                tile = Tile(("º","o"),((self.FLOWER_RED),(bg)),True,16)
            elif roll <= 47:
                tile = Tile(("º","o"),((self.FLOWER_BLUE),(bg)),True,16)
            else:
                tile = Tile(("º","o"),((self.FLOWER_PURPLE),(bg)),True,16)
        elif roll == 2:
            tile = Tile("*",((self.GRASS_TALL),(bg)))
        else:
            tile = Tile((".",","),((self.GRASS_TALL),(bg)),True,16)
        return tile

class WetPlains(Biome):
    def __init__(self):
        self.GRASS_LIGHTER = (120, 196, 43)
        self.GRASS_LIGHT = (111, 182, 40)
        self.GRASS_TALL = (69, 114, 25)
        self.WEED = (224, 140, 49)
        self.PUDDLE_SHALLOW = (49, 178, 224)
        self.PUDDLE_DEEP = (49, 67, 224)
    def generate(self, cords, seed):
        y, x = cords
        random.seed(str((y, x, seed)))
        gradient = noise.pnoise2(y / 12, x / 12, octaves=4, persistence=1,base=seed)
        if gradient >= -0.10:
            if gradient >= 0.15:
                bg = self.GRASS_LIGHTER
            else:
                bg = self.GRASS_LIGHT
            roll = random.randint(1,8)
            if roll == 1:
                tile = Tile(("-","~"),((self.PUDDLE_DEEP),(self.PUDDLE_SHALLOW)),True,16)
            elif roll == 2:
                tile = Tile("*",((self.WEED),(bg)))
            else:
                tile = Tile((".",","),((self.GRASS_TALL),(bg)),True,16)
        elif gradient >= -0.25:
            tile = Tile(("-","~"),((self.PUDDLE_DEEP),(self.PUDDLE_SHALLOW)),True,16)
        else:
            tile = Tile(("-","~"),((self.PUDDLE_SHALLOW),(self.PUDDLE_DEEP)),False,16)
        return tile
    
class DryPlains(Biome):
    def __init__(self):
        self.GRASS_LIGHTER = (230, 205, 129)
        self.GRASS_LIGHT = (230, 192, 129)
        self.GRASS_TALL = (230, 159, 129)
        self.FLOWER_PINK = (230, 129, 90)
    def generate(self, cords, seed):
        y, x = cords
        random.seed(str((y, x, seed)))
        gradient = noise.pnoise2(y / 12, x / 12, octaves=4, persistence=1,base=seed)
        if gradient >= 0:
            bg = self.GRASS_LIGHT
        else:
            bg = self.GRASS_LIGHTER
        roll = random.randint(1,24)
        if roll == 1:
            tile = Tile(("º","o"),((self.FLOWER_PINK),(bg)),True,16)
        elif roll <= 4:
            tile = Tile("*",((self.GRASS_TALL),(bg)))
        else:
            tile = Tile((".",","),((self.GRASS_TALL),(bg)),True,16)
        return tile

class Forest(Biome):
    def __init__(self):
        self.GRASS_LIGHT = (65, 106, 23)
        self.GRASS = (70, 115, 25)
        self.GRASS_TALL = (37, 51, 24)
        self.MUSHROOM_RED = (128, 12, 12)
        self.MUSHROOM_PURPLE = (104, 25, 115)
        self.MUSHROOM_GLOWING = (255, 255, 128)
    def generate(self, cords, seed):
        y, x = cords
        random.seed(str((y, x, seed)))
        gradient = noise.pnoise2(y / 12, x / 12, octaves=4, persistence=1,base=seed)
        if gradient >= 0:
            bg = self.GRASS
        else:
            bg = self.GRASS_LIGHT
        roll = random.randint(1,32)
        if roll == 1:
            roll = random.randint(1,48)
            if roll <= 38:
                tile = Tile("o",((self.MUSHROOM_RED),(bg)))
            elif roll <= 47:
                tile = Tile("o",((self.MUSHROOM_PURPLE),(bg)))
            else:
                tile = Tile("o",((self.MUSHROOM_GLOWING),(bg)))
        elif roll <= 5:
            tile = Tile("*",((self.GRASS_TALL),(bg)))
        else:
            tile = Tile((".",","),((self.GRASS_TALL),(bg)),True,16)
        return tile