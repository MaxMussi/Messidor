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
    
class Entity:
    def __init__(self, chars, colors,cords, health, simple=True, animSpd=0):
        self.chars = chars
        self.colors = colors
        self.cords = cords
        self.health = health
        self.simple = simple
        self.animSpd = animSpd

class Player(Entity):
    def __init__(self, chars, colors, cords, animSpd, name, health, hunger, thirst):
        super().__init__(chars, colors, cords, health, animSpd)
        self.name = name
        self.hunger = hunger
        self.thirst = thirst
        self.passable = False

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