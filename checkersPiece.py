class Piece():
    def __init__(self, color, id):
        self.color = color
        self.id = color + str(id)
        self.pos = None
        self.king = False
        pass