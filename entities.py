class Player:
    def __init__(self, name, color, cordY, cordX):
        self.name = name
        self.char = "@"
        self.color = color
        self.cordX = cordX
        self.cordY = cordY
    def controls(self, key, map_data):
        if key == ord("w") and map_data[self.cordY - 1][self.cordX].passable == True:
            self.cordY -= 1
        elif key == ord("a") and map_data[self.cordY][self.cordX - 1].passable == True:
            self.cordX -= 1
        elif key == ord("s") and map_data[self.cordY + 1][self.cordX].passable == True:
            self.cordY += 1
        elif key == ord("d") and map_data[self.cordY][self.cordX + 1].passable == True:
            self.cordX += 1