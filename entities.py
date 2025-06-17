class Player:
    def __init__(self, name, char ,color, cords):
        self.name = name
        self.char = char
        self.color = color
        self.cords = cords
    
    def controls(self, key, map_data, map_cords):
        mapCordY, mapCordX = map_cords
        playerCordY, playerCordX = self.cords
        if key == ord("w") and map_data[mapCordY - 1][mapCordX].passable == True:
            self.cords = (playerCordY - 1, playerCordX)
        elif key == ord("a") and map_data[mapCordY][mapCordX - 1].passable == True:
            self.cords = (playerCordY, playerCordX - 1)
        elif key == ord("s") and map_data[mapCordY + 1][mapCordX].passable == True:
            self.cords = (playerCordY + 1, playerCordX)
        elif key == ord("d") and map_data[mapCordY][mapCordX + 1].passable == True:
            self.cords = (playerCordY, playerCordX + 1)
