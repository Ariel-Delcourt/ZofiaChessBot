class Piece:

    def __init__(self, team, mailbox):
        self.mailbox = mailbox              # Its location on the board
        self.team = team                    # White/Black
        self.offsets = []
        self.legalMoves = []
        self.xray = {}                     # Array of pieces attacked indirectly through another (x-ray vision)

    def xraySearch(self,offset,target,board):
        currentXray = []
        while (board[target].mailbox > 0):    # Depth search - sees behind the piece until out of bounds
            if board[target].piece is not None:
                currentXray.append(board[target].piece)
            target += offset
        if currentXray != []:
            self.xray[offset] = currentXray

class Pawn(Piece):

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)
        self.name = 'P'
        self.value = 1

    # Generates pawn moves, this one is different from the line of sight pieces, and so has its own move generation method
    # legal moves are stored in an array of tuples given by (coordinate of piece, action, coordinate of move),
    # where action can be one of: 'move', 'capture', or 'castle'.
    def generateMoves(self, board):
        legalMoves = []                                         
        if (self.team == 'white'):                              # For team white, pawn moves up
            #---- QUIET MOVES ----#
            capture = [9,11]                                     # Only possible capture moves for pawn (TODO: en passant)
            if (board[self.mailbox + 10].piece is None):         # Checks for obstructing piece in front
                if (board[self.mailbox + 10].mailbox > 0):      # Checks out of bounds
                    legalMoves.append(('move', self.mailbox + 10))
                if (30 < self.mailbox < 39):                     # Checks for double move option
                    if (board[self.mailbox + 20].piece is None):
                        legalMoves.append(('doubleMove', self.mailbox + 20))
            #---- CAPTURE MOVES ----#
            for offset in capture:                              # Checks all capture possibilities
                if (board[self.mailbox + offset].piece is not None):
                    if (board[self.mailbox + offset].piece.team == 'black'):
                        if (board[self.mailbox + offset].mailbox > 0): # Checks out of bounds
                            legalMoves.append(('capture', self.mailbox + offset))

        else:                                                   # For team black, pawn moves down
            #---- QUIET MOVES ----#
            capture = [-11,-9]                                    # Only possible capture moves for pawn (TODO: en passant)
            if (board[self.mailbox - 10].piece is None):         # Checks for obstructing piece in front
                if (board[self.mailbox - 10].mailbox > 0):      # Checks for out of bounds move
                    legalMoves.append(('move', self.mailbox - 10))
                if (80 < self.mailbox < 89):                     # Checks for double move option
                    if (board[self.mailbox - 20].piece is None):
                        legalMoves.append(('doubleMove', self.mailbox - 20))
            #---- CAPTURE MOVES ----#
            for offset in capture:                              # Checks all capture possibilities
                if (board[self.mailbox + offset].piece is not None):
                    if (board[self.mailbox + offset].piece.team == 'white'):
                        if (board[self.mailbox + offset].mailbox > 0):         # Checks out of bounds
                            legalMoves.append(('capture', self.mailbox + offset))
        self.legalMoves = legalMoves
    
class Knight(Piece):

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)
        self.name = 'N'
        self.value = 3

    def generateMoves(self, board):
        self.legalMoves = []
        offsets = [19,21,8,12,-8,-12,-19,-21]
        for offset in offsets:
            if (board[self.mailbox + offset].mailbox > 0):
                if (board[self.mailbox + offset].piece is None):
                    self.legalMoves.append(('move', self.mailbox + offset))
                elif (board[self.mailbox + offset].piece.team != self.team):
                    self.legalMoves.append(('capture', self.mailbox + offset))
        
class King(Piece):

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)
        self.name = 'K'
        self.value = float("inf")               # The king has infinite value, useful for move consideration

    def cullUnsafeMoves(self,board):
        newLegalMoves = []
        if (self.team == 'white'):
            for move, target in self.legalMoves:
                if (len(board[target].watchedBy['black']) == 0):
                    newLegalMoves.append((move,target))
        else:
            for move, target in self.legalMoves:
                if (len(board[target].watchedBy['white']) == 0):
                    newLegalMoves.append((move,target))
        self.legalMoves = newLegalMoves

    def generateMoves(self, board):
        self.legalMoves = []
        offsets = [1,11,10,9,-1,-11,-10,-9]
        for offset in offsets:
            if (board[self.mailbox + offset].mailbox > 0):
                if (board[self.mailbox + offset].piece is None):
                    self.legalMoves.append(('move', self.mailbox + offset))
                elif (board[self.mailbox + offset].piece.team != self.team):
                    self.legalMoves.append(('capture', self.mailbox + offset))

class Bishop(Piece):

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)
        self.name = 'B'
        self.value = 3
        self.offsets = [9,11,-9,-11]

    def generateMoves(self, board):
        legalMoves = []
        self.xray = {}                  #Clears previously x-rayed pieces
        for offset in self.offsets:        #For each possible move direction
            target = self.mailbox + offset
            # This loop moves tile by tile, assessing the presence of a piece or out of bounds
            # If a piece is found, it attempts to see the pieces behind it, accounting for pins and xray attacks
            while ((board[target].mailbox > 0) and (board[target].piece is None)):
                legalMoves.append(('move', target))   # Format for move storage: ('move'/'capture', mailbox of where move would put this piece)
                target += offset
            if (board[target].piece is not None):
                if (board[target].piece.team != self.team):
                    legalMoves.append(('capture', target))
                self.xraySearch(offset,target,board)
        self.legalMoves = legalMoves

class Rook(Piece):

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)
        self.name = 'R'
        self.value = 5
        self.offsets = [1,-1,10,-10]

    def generateMoves(self, board):
        legalMoves = []
        self.xray = {}                  #Clears previously x-rayed pieces
        for offset in self.offsets:        #For each possible move direction
            target = self.mailbox + offset
            # This loop moves tile by tile, assessing the presence of a piece or out of bounds
            # If a piece is found, it attempts to see the pieces behind it, accounting for pins and xray attacks
            while ((board[target].mailbox > 0) and (board[target].piece is None)):
                legalMoves.append(('move', target))   # Format for move storage: ('move'/'capture', mailbox of where move would put this piece)
                target += offset
            if (board[target].piece is not None):
                if (board[target].piece.team != self.team):
                    legalMoves.append(('capture', target))
                self.xraySearch(offset,target,board)
        self.legalMoves = legalMoves
            

class Queen(Piece):

    def __init__(self, team, mailbox):
        super().__init__(team, mailbox)
        self.name = 'Q'
        self.value = 9
        self.offsets = [1,11,10,9,-1,-11,-10,-9]
    
    def generateMoves(self, board):
        legalMoves = []
        self.xray = {}                  #Clears previously x-rayed pieces
        for offset in self.offsets:        #For each possible move direction
            target = self.mailbox + offset
            # This loop moves tile by tile, assessing the presence of a piece or out of bounds
            # If a piece is found, it attempts to see the pieces behind it, accounting for pins and xray attacks
            while ((board[target].mailbox > 0) and (board[target].piece is None)):
                legalMoves.append(('move', target))   # Format for move storage: ('move'/'capture', mailbox of where move would put this piece)
                target += offset
            if (board[target].piece is not None):
                if (board[target].piece.team != self.team):
                    legalMoves.append(('capture', target))
                self.xraySearch(offset,target,board)
        self.legalMoves = legalMoves