from checkersPlayer import Player
from checkersPiece import Piece

DEFAULT_AI_FILE = "checkersPlayer"
DEFAULT_COLUMNS = 8
DEFAULT_ROWS = 8

class CheckerBoard():
    def __init__(self, num_columns, num_rows):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.matrix = None
    
    def playGame(self):
        pass
    
    def legalMoveExists(self):
        pass
    
    '''
    This function takes itself, a checkers board, the row and column, and the piece, and
    places the piece at row and column on the board
    '''
    def placeDisc(self, board, row, column, piece):
        board[row][column] = piece.id
    
    def initializeBoard(self, columns, rows):
        matrix = [['---' for _ in range(columns)] for _ in range(rows)]
        return matrix
    
    def initRed(self, columns, rows):
        
        id = 1
        # iterate through the board and place the red pieces
        for i in range(rows):
            
            for j in range(columns):
                if i % 2 != 0:
                    if j % 2 == 0:
                        newPiece = Piece('R', id)
                        self.placeDisc(self.matrix, i, j, newPiece)
                        id += 1
                else:
                    if j % 2 != 0:
                        newPiece = Piece('R', id)
                        self.placeDisc(self.matrix, i, j, newPiece)
                        id += 1
            
            if id >= 12: break
            
        return self.matrix
                
    def initWhite(self, columns, rows):

        id = 1
        # iterate through the board and place the red pieces
        for i in range(rows-1, 0, -1):
            
            for j in range(columns):
                if i % 2 != 0:
                    if j % 2 == 0:
                        newPiece = Piece('W', id)
                        self.placeDisc(self.matrix, i, j, newPiece)
                        id += 1
                else:
                    if j % 2 != 0:
                        newPiece = Piece('W', id)
                        self.placeDisc(self.matrix, i, j, newPiece)
                        id += 1
            
            if id >= 12: break
            
        return self.matrix
    
    def buildBoard():
        theBoard = CheckerBoard(DEFAULT_COLUMNS,DEFAULT_ROWS)
        theBoard.matrix = theBoard.initializeBoard(DEFAULT_COLUMNS,DEFAULT_ROWS)
        theBoard.matrix = theBoard.initRed(DEFAULT_COLUMNS,DEFAULT_ROWS)
        theBoard.matrix = theBoard.initWhite(DEFAULT_COLUMNS,DEFAULT_ROWS)
        
        return theBoard
    
    '''
    This function takes itself and the board. It then prints the current state of the board
    '''
    def printBoard(self, board):
        
        for i, elem in enumerate(board):
            for j, item in enumerate(elem):
                print(item, end=' ')
            print()
    
    def aiTurn(self):
        pass
    
    
def main():
    theBoard = CheckerBoard.buildBoard()
    theBoard.printBoard(theBoard.matrix)
    
if __name__ == "__main__":
    main()