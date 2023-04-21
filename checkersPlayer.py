DEFAULT_PIECES = 12

class Player():
    def __init__(self, id, difficulty_level, color):
        self.id = id
        self.difficulty_level = difficulty_level
        self.num_pieces = DEFAULT_PIECES
        self.color = color
        self.ab = True
    
    def pick_move(self, board):
        pass
    
    def minimax(self, board, player, difficulty, alpha, beta, ab):
        
        if difficulty == 0:
            pass
    
    '''
    This function takes itself and a board. It then checks to see whether one color remains or if
    there are any more legal moves you can make
    '''
    def gameDone(self, board):
        
        isDone = False
        positions = []
        for i in board:
            row = [value for value in i if value != '---']
            positions = positions + row
            
        if len(set(positions)) == 1:
            isDone = True
        
        # add in function for checking if there are any legal moves
        
        return isDone
            
        
    def isLegalMoveLeft(self, board):
        pass
        
     
    def getChildren(self, board, player):
        
        if player == 1:
            
            pass
        
        if player == 2:
            pass
        
    def evaluateScore(self, board, player):
        
        if player == 1:
            pass
        else:
            pass
        
    '''
    This function takes itself, the current board state, and the player. The function
    then calculates the score for the player using this heuristic:
        - Count the number of pieces each player has on the board (addition for the AI
          and subtraction for the human player).
        - If any pieces are "kinged", add/subtract an additional weight to the piece
        - The closer a piece is to the opposing side, add/subtract additional weight to 
          include how close the piece is to becoming "kinged"
    '''
    def heuristic(self, board, player):
        
        row = len(board)
        height = len(board[0])
        score = 0
        if player == 1:
            for i, elem in enumerate(board):
                score += elem.count(1)
                score += elem.count(2) * 2 # if there are kings
                    
        if player == -1:
            for i, elem in enumerate(board):
                score -= elem.count(-1)
                score -= elem.count(-2) * 2 # if there are kings
                
                
                
        
        
    
    def findOpenLocation():
        pass