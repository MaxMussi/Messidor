import random
from terrain import World

MOVES = {
    ord("w"): (-1, 0),
    ord("a"): (0, -1),
    ord("s"): (1, 0),
    ord("d"): (0, 1),
}

def isFree(mapData, entityData, cordY, cordX):
    if getattr(mapData.get((cordY,cordX),None), "passable", True) and getattr(entityData.get((cordY,cordX),None), "passable", True):
        return True
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

        roll = random.randint(1,2048)
        if roll <= self.spawnRate:
            self.data[cords] = Rabbit("r",((255,255,255),None),cords,15)
        
        return self.data[cords]
    
class Entity:
    def __init__(self, chars, colors,cords, health):
        self.chars = chars
        self.colors = colors
        self.cords = cords
        self.health = health
        self.passable = False

class Player(Entity):
    def __init__(self, chars, colors, cords, name, health, hunger, thirst):
        super().__init__(chars, colors, cords, health)
        self.name = name
        self.hunger = hunger
        self.thirst = thirst
        self.passable = False

    def controls(self, key,mapData, entityData, scrCords):
        dy, dx = MOVES.get(key, (0, 0))
        newY = self.cords[0] + dy
        newX = self.cords[1] + dx
        if (dy != 0 or dx != 0) and isFree(mapData, entityData, newY, newX):
            self.cords = (newY, newX)
            return True
        return False

class Creature(Entity):
    def __init__(self, chars, colors, cords, health):
        super().__init__(chars, colors, cords, health)

    def tickAi(self, mapData, entityData):
        pass

class Rabbit(Creature):
    def __init__(self, chars, colors, cords, health):
        super().__init__(chars, colors, cords, health)
    
    def tickAi(self, mapData, entityData):
        cordY, cordX = self.cords
        roll = random.randint(0, 7)
        knight_moves = [(1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]
        dY, dX = knight_moves[roll]
        newY, newX = cordY + dY, cordX + dX
        roll = random.randint(0,1)
        if self.health > 10 and roll == 0:
            return None
        if isFree(mapData, entityData, newY, newX):
            self.cords = (newY, newX)