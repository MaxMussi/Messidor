import random
from terrain import World

MOVES = {
    ord("w"): (-1, 0),
    ord("a"): (0, -1),
    ord("s"): (1, 0),
    ord("d"): (0, 1),
}

def isFree(playerCords, mapData, entityData, cordY, cordX):
    if getattr(mapData.get((cordY,cordX),None), "passable", True):
        if entityData.get((cordY,cordX), None) is not None:
            if getattr(entityData.get((cordY,cordX), None), "passable"):
                return True
            return None
        elif (cordY, cordX) == playerCords:
            return False
        else:
            return True
    return False

def attack(attacker, attacked):
    if getattr(attacker, "inventory") is not None:
        weapon = attacker.inventory.get("weapon", None)
        if weapon is not None:
            attacked.health -= getattr(weapon, "damage", 0)
            attacked.stunTimer = 6
        else:
            attacked.health -= attacker.damage
            attacked.stunTimer = 6
    elif getattr(attacker, "damage") is not None:
        attacked.health -= attacker.damage
        attacked.stunTimer = 6

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
    def __init__(self, chars, colors, cords, health):
        self.chars = chars
        self.colors = colors
        self.cords = cords
        self.health = health
        self.inventory = {}

class Player(Entity):
    def __init__(self, chars, colors, cords, name, health, hunger, thirst):
        super().__init__(chars, colors, cords, health)
        self.name = name
        self.hunger = hunger
        self.thirst = thirst
        self.damage = 6
        self.stunTimer = 0

    def controls(self, key, mapData, entityData):
        dy, dx = MOVES.get(key, (0, 0))
        newY = self.cords[0] + dy
        newX = self.cords[1] + dx
        if (dy != 0 or dx != 0):
            free = isFree(self.cords, mapData, entityData, newY, newX)
            if free:
                self.cords = (newY, newX)
                return True
            elif free is None:
                attack(self, entityData[newY,newX])
                return True
        return False

    def resetColors(self):
        self.colors = ((255,255,0),None)

class Creature(Entity):
    def __init__(self, chars, colors, cords, health, damage=0):
        super().__init__(chars, colors, cords, health)
        self.stunTimer = 0
        self.passable = False
        self.damage = damage

    def tickAi(self, mapData, entityData):
        pass
    def resetColors():
        pass

class Rabbit(Creature):
    def __init__(self, chars, colors, cords, health):
        super().__init__(chars, colors, cords, health)
    
    def tickAi(self, mapData, entityData, playerCords):
        cordY, cordX = self.cords
        roll = random.randint(0, 7)
        knight_moves = [(1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]
        dY, dX = knight_moves[roll]
        newY, newX = cordY + dY, cordX + dX
        roll = random.randint(1,4)
        if (self.health < 10 or roll == 1) and isFree(playerCords, mapData, entityData, newY, newX):
            self.cords = (newY, newX) 
    def resetColors(self):
        self.colors = ((255,255,255),None)