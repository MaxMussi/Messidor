import random

MOVES = {
    ord("w"): (-1, 0),
    ord("a"): (0, -1),
    ord("s"): (1, 0),
    ord("d"): (0, 1),
}

def isFree(mapData, entityData, cordY, cordX):
    try:
        if mapData[cordY][cordX].passable == True and entityData[cordY][cordX] is None:
            return True
        return False
    except:
        return False

class Spawner:
    def __init__(self, spawnRate, world):
        self.spawnRate = spawnRate
        self.world = world
        self.data = {}

    def attemptSpawn(self, cords):
        if cords in self.data:
            return self.data[cords]

        self.data[cords] = None
        layeredNoise = self.world.getLayeredNoise(cords)
        biome = self.world.getBiome(layeredNoise)

        roll = random.randint(1, 2400)
        if roll <= self.spawnRate:
            self.data[cords] = Rabbit("r", ((255,255,255), None), cords, 15, False)

        return self.data[cords]

    
class Entity:
    def __init__(self, chars, colors,cords, health, hostile=False):
        self.chars = chars
        self.colors = colors
        self.cords = cords
        self.health = health
        self.hostile = hostile
        self.passable = False

class Player(Entity):
    def __init__(self, chars, colors, cords, name, health, hunger, thirst):
        super().__init__(chars, colors, cords, health)
        self.name = name
        self.hunger = hunger
        self.thirst = thirst

    def controls(self, key, mapData, entityData, wolrdCords):
        dy, dx = MOVES.get(key, (0, 0))
        newY = self.cords[0] + dy
        newX = self.cords[1] + dx
        mapY = wolrdCords[0] + dy
        mapX = wolrdCords[1] + dx
        if isFree(mapData, entityData, mapY, mapX):
            self.cords = (newY, newX)
            return True
        return False

class Creature(Entity):
    def __init__(self, chars, colors, cords, health, hostile=False):
        super().__init__(chars, colors, cords, health, hostile)

    def tickAi(self, fgData, bgData):
        pass

class Rabbit(Creature):
    def __init__(self, char, color, cords, health, hostile):
        super().__init__(char, color, cords, health, hostile)

    def tickAi(self, bgData, fgData):
        y, x = self.cords
        roll = random.randint(0, 7)
        knight_moves = [(1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]
        dy, dx = knight_moves[roll]
        newY, newX = y + dy, x + dx
        if self.health < 15:
            if isFree(bgData, fgData, newY, newX):
                self.cords = (newY, newX)
        else:
            roll = random.randint(0,1)
            if roll == 1:
                if isFree(bgData, fgData, newY, newX):
                    self.cords = (newY, newX)