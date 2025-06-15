class Player:
    def __init__(self, name, color, cordY, cordX):
        self.name = name
        self.char = "@"
        self.color = color
        self.cordX = cordX
        self.cordY = cordY
    def controls(self, key):
        if key == ord("w"):
            self.cordY -= 1
        elif key == ord("a"):
            self.cordX -= 1
        elif key == ord("s"):
            self.cordY += 1
        elif key == ord("d"):
            self.cordX += 1