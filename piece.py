class Piece:

    def __init__(self, team, mailbox):
        self.mailbox = mailbox              # Its location on the board
        self.team = team                    # White/Black
        self.xray = []                      # Array of pieces attacked indirectly through another (x-ray vision)

class Pawn(Piece):

    name = 'P'
    value = 1
    pinned = False

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)

    def generateMoves(self, board):
        legalMoves = []                                         #legal moves are stored in an array of tuples given by (coordinate of piece, action, coordinate of move),
                                                                #where action can be one of: 'move', 'capture', or 'castle'.
        if (self.team == 'white'):                              #For team white, pawn moves up
            #---- QUIET MOVES ----#
            capture = [9,11]                                     #Only possible capture moves for pawn (TODO: en passant)
            if (board[self.mailbox + 10].piece is None):         #Checks for obstructing piece in front
                if (board[self.mailbox + 10].mailbox > 0):      #Checks out of bounds
                    legalMoves.append(('move', self.mailbox + 10))
                if (30 < self.mailbox < 39):                     #Checks for double move option
                    if (board[self.mailbox + 20].piece is None):
                        legalMoves.append(('move', self.mailbox + 20))
            #---- CAPTURE MOVES ----#
            for offset in capture:                              #Checks all capture possibilities
                if (board[self.mailbox + offset].piece is not None):
                    if (board[self.mailbox + offset].piece.team == 'black'):
                        if (board[self.mailbox + offset].mailbox > 0): #Checks out of bounds
                            legalMoves.append(('capture', self.mailbox + offset))

        else:                                                   #For team black, pawn moves down
            #---- QUIET MOVES ----#
            capture = [-11,-9]                                    #Only possible capture moves for pawn (TODO: en passant)
            if (board[self.mailbox - 10].piece is None):         #Checks for obstructing piece in front
                if (board[self.mailbox - 10].mailbox > 0):      #Checks for out of bounds move
                    legalMoves.append(('move', self.mailbox - 10))
                if (80 < self.mailbox < 89):                     #Checks for double move option
                    if (board[self.mailbox - 20].piece is None):
                        legalMoves.append(('move', self.mailbox - 20))
            #---- CAPTURE MOVES ----#
            for offset in capture:                              #Checks all capture possibilities
                if (board[self.mailbox + offset].piece is not None):
                    if (board[self.mailbox + offset].piece.team == 'white'):
                        if (board[self.mailbox + offset].mailbox > 0):         #Checks out of bounds
                            legalMoves.append(('capture', self.mailbox + offset))
        self.legalMoves = legalMoves
    
class Knight(Piece):

    name = 'N'
    value = 3
    pinned = False

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)

    def generateMoves(self, board):
        legalMoves = []
        offsets = [19,21,8,12,-8,-12,-19,-21]
        for offset in offsets:
            if (board[self.mailbox + offset].mailbox > 0):
                if (board[self.mailbox + offset].piece is None):
                    legalMoves.append(('move', self.mailbox + offset))
                elif (board[self.mailbox + offset].piece.team != self.team):
                    legalMoves.append(('capture', self.mailbox + offset))
        self.legalMoves = legalMoves
        
class King(Piece):

    name = 'K'
    value = float("inf")
    pinned = False

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)

    def generateMoves(self, board):
        legalMoves = []
        offsets = [1,11,10,9,-1,-11,-10,-9]
        for offset in offsets:
            if (board[self.mailbox + offset].mailbox > 0):
                if (board[self.mailbox + offset].piece is None):
                    legalMoves.append(('move', self.mailbox + offset))
                elif (board[self.mailbox + offset].piece.team != self.team):
                    legalMoves.append(('capture', self.mailbox + offset))
        self.legalMoves = legalMoves

class Bishop(Piece):

    name = 'B'
    value = 3
    pinned = False

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)

    def generateMoves(self, board):
        legalMoves = []
        offsets = [9,11,-9,-11]
        for offset in offsets:
            newOffset = offset
            while ((board[self.mailbox + newOffset].mailbox > 0) and (board[self.mailbox + newOffset].piece is None)):
                legalMoves.append(('move', self.mailbox + newOffset))
                newOffset += offset
            if (board[self.mailbox + newOffset].piece is not None):
                if (board[self.mailbox + newOffset].piece.team != self.team):
                    legalMoves.append(('capture', self.mailbox + newOffset))
        self.legalMoves = legalMoves

class Rook(Piece):

    name = 'R'
    value = 5
    pinned = False

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)

    def generateMoves(self, board):
        legalMoves = []
        offsets = [1,-1,10,-10]
        for offset in offsets:
            newOffset = offset
            while ((board[self.mailbox + newOffset].mailbox > 0) and (board[self.mailbox + newOffset].piece is None)):
                legalMoves.append(('move', self.mailbox + newOffset))
                newOffset += offset
            if (board[self.mailbox + newOffset].piece is not None):
                if (board[self.mailbox + newOffset].piece.team != self.team):
                    legalMoves.append(('capture', self.mailbox + newOffset))
        self.legalMoves = legalMoves
            

class Queen(Piece):

    name = 'Q'
    value = 9
    pinned = False

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)
    
    def generateMoves(self, board):
        legalMoves = []
        offsets = [1,11,10,9,-1,-11,-10,-9]
        for offset in offsets:
            newOffset = offset
            while ((board[self.mailbox + newOffset].mailbox > 0) and (board[self.mailbox + newOffset].piece is None)):
                legalMoves.append(('move', self.mailbox + newOffset))
                newOffset += offset
            if (board[self.mailbox + newOffset].piece is not None):
                if (board[self.mailbox + newOffset].piece.team != self.team):
                    legalMoves.append(('capture', self.mailbox + newOffset))
        self.legalMoves = legalMoves