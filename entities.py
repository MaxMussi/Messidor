import random

MOVES = {
    ord("w"): (-1, 0),
    ord("a"): (0, -1),
    ord("s"): (1, 0),
    ord("d"): (0, 1),
}

def isFree(map_data, entity_data, mapCordY, mapCordX):
    try:
        if map_data[mapCordY][mapCordX].passable:
            entity = entity_data[mapCordY][mapCordX]
            return entity is None or getattr(entity, "passable", False)
        return False
    except:
        return False
    
class Entity:
    def __init__(self, char, color, cords, health):
        self.char = char
        self.color = color
        self.cords = cords
        self.health = health

class Player(Entity):
    def __init__(self, name, char, color, cords, health, hunger, thirst):
        super().__init__(char, color, cords, health)
        self.name = name
        self.hunger = hunger
        self.thirst = thirst
        self.passable = False

    def controls(self, key, map_data, entity_data, map_cords):
        dy, dx = MOVES.get(key, (0, 0))
        newY = self.cords[0] + dy
        newX = self.cords[1] + dx
        mapY = map_cords[0] + dy
        mapX = map_cords[1] + dx
        if isFree(map_data, entity_data, mapY, mapX):
            self.cords = (newY, newX)

class Creature(Entity):
    def __init__(self, char, color, cords, health, hostile, passable):
        super().__init__(char, color, cords, health)
        self.aggresive = hostile
        self.passable = passable

    def tickAi(self, map_data, entity_data):
        pass

class Rabbit(Creature):
    def __init__(self, char, color, cords, health, hostile, passable):
        super().__init__(char, color, cords, health, hostile, passable)

    def tickAi(self, map_data, entity_data):
        y, x = self.cords
        gradient = random.randint(0, 7)
        knight_moves = [(1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]
        dy, dx = knight_moves[gradient]
        newY, newX = y + dy, x + dx
        if isFree(map_data, entity_data, newY, newX):
            self.cords = (newY, newX)


class Spawner:
    def __init__(self, passiveSpawnRate, hostileSpawnRate):
        self.passiveSpawnRate = passiveSpawnRate
        self.hostileSpawnRate = hostileSpawnRate
        self.data = {}

    def getMob(self, cords, world):
        if cords in self.data:
            return self.data[cords]
        
        self.data[cords] = None
        layeredNoise = world.getLayeredNoise(cords)
        biome = world.getBiome(layeredNoise)
        gradient = random.randint(1, 24000)

        if biome == "Forest":
            if gradient <= self.passiveSpawnRate:
                self.data[cords] = Rabbit("r", (7, -1), cords, 5, False, False)

        return self.data[cords]
