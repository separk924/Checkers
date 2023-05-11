'''
This class creates a constructor for a single Checkers Piece
'''
class Piece():
    '''
    CONSTRUCTOR: This constructor takes a color ('B' for black and 'R' for red), an int id, and
    a status for whether it has been kinged or not.
    '''
    def __init__(self, color, id, status):
        self.color = color
        self.id = color + str(id)
        self.status = status
        self.pos = None
        self.moves = []