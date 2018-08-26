from tile import Tile
from piece import *
from colorama import Fore, Back, init
init()

class Board:
    
    def __init__(self):
        self.board = []
        self.canCastle = {'black':{'kingside':False, 'queenside':False}, 'white': {'kingside':False, 'queenside':False}}
        self.currentTurn = 0
        self.playerTurnToPlay = 'white'
        self.enPassantSquare = None
        
    def makeBoard(self):
        finalBoard = []
        board = [
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, 21, 22, 23, 24, 25, 26, 27, 28, -1,
            -1, 31, 32, 33, 34, 35, 36, 37, 38, -1,
            -1, 41, 42, 43, 44, 45, 46, 47, 48, -1,
            -1, 51, 52, 53, 54, 55, 56, 57, 58, -1,
            -1, 61, 62, 63, 64, 65, 66, 67, 68, -1,
            -1, 71, 72, 73, 74, 75, 76, 77, 78, -1,
            -1, 81, 82, 83, 84, 85, 86, 87, 88, -1,
            -1, 91, 92, 93, 94, 95, 96, 97, 98, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
            ]
        for i in board:
            finalBoard.append(Tile('x', i, None))
        self.board = finalBoard

    def clearBoard(self):
        for tile in self.board:
            tile.piece = None

    def populate(self):
        for i in range(31,39):
            self.board[i].piece = Pawn('white', self.board[i].mailbox)
        for i in range(81,89):
            self.board[i].piece = Pawn('black', self.board[i].mailbox)
        for i in [21,28]:
            self.board[i].piece = Rook('white', self.board[i].mailbox)
        for i in [91,98]:
            self.board[i].piece = Rook('black', self.board[i].mailbox)
        for i in [22,27]:
            self.board[i].piece = Knight('white', self.board[i].mailbox)
        for i in [92,97]:
            self.board[i].piece = Knight('black', self.board[i].mailbox)
        for i in [23,26]:
            self.board[i].piece = Bishop('white', self.board[i].mailbox)
        for i in [93,96]:
            self.board[i].piece = Bishop('black', self.board[i].mailbox)
        self.board[24].piece = Queen('white', self.board[24].mailbox)
        self.board[94].piece = Queen('black', self.board[94].mailbox)
        self.board[25].piece = King('white', self.board[25].mailbox)
        self.board[95].piece = King('black', self.board[95].mailbox)
        self.canCastle['white']['kingside'] = True
        self.canCastle['white']['queenside'] = True
        self.canCastle['black']['kingside'] = True
        self.canCastle['black']['queenside'] = True
        self.currentTurn = 1
        self.playerTurnToPlay = 'white'

    def display(self):
        counter = 0
        displayArray = []
        currentRank = []
        for tile in self.board:
            currentRank.append(tile)
            if (counter > 8):
                displayArray.insert(0, currentRank)
                counter = 0
                currentRank = []
            else:
                counter += 1

        for rank in displayArray:
            for tile in rank:
                if (tile.piece is None):
                    print(Fore.WHITE + '-', end=" ", flush=True)
                elif (tile.piece.team == 'white'):
                    print(Fore.WHITE + tile.piece.name, end=" ", flush=True)
                else:
                    print(Fore.LIGHTYELLOW_EX + tile.piece.name, end=" ", flush=True)
            print()

    def addPiece(self, piece, team, mailbox):
        piece = str.capitalize(piece)
        team = str.lower(team)
        if type(mailbox) is str:
            mailbox = Tile.coordinateToMailbox(mailbox)
        if (piece == 'P'):
            self.board[mailbox].piece = Pawn(team, mailbox)
            print("Successfully added", team,"Pawn to", mailbox)
        elif (piece == 'R'):
            self.board[mailbox].piece = Rook(team, mailbox)
            print("Successfully added", team,"Rook to", mailbox)
        elif (piece == 'N'):
            self.board[mailbox].piece = Knight(team, mailbox)
            print("Successfully added", team,"Knight to", mailbox)
        elif (piece == 'B'):
            self.board[mailbox].piece = Bishop(team, mailbox)
            print("Successfully added", team,"Bishop to", mailbox)
        elif (piece == 'Q'):
            self.board[mailbox].piece = Queen(team, mailbox)
            print("Successfully added", team,"Queen to", mailbox)
        elif (piece == 'K'):
            self.board[mailbox].piece = King(team, mailbox)
            print("Successfully added", team,"King to", mailbox)
        else:
            print("Incorrect piece code")
    
    def generatePieceList(self):        # Generates multi-level dictionary containing objects of all pieces on the board
        pieceList = {
            'white': {'P': {}, 'N': {}, 'B': {}, 'R': {}, 'Q': {}, 'K': {}},
            'black': {'P': {}, 'N': {}, 'B': {}, 'R': {}, 'Q': {}, 'K': {}}
            }
        
        for tile in self.board:
            if (tile.piece is not None):
                pieceList[tile.piece.team][tile.piece.name][tile.piece.mailbox] = tile.piece
        self.pieceList = pieceList

    def generateAllMoves(self):                              # Generates moves for all pieces on the board (stored in each piece's legalmoves array)
        legalMovesList = self.pieceList                   # Does not account for pins, en passant, or castling
        for pieceName in legalMovesList['white'].items():
            for mailbox in pieceName[1]:
                pieceName[1][mailbox].generateMoves(self.board)
        for pieceName in legalMovesList['black'].items():
            for mailbox in pieceName[1]:
                pieceName[1][mailbox].generateMoves(self.board)
    
    def markBoardTiles(self):
        legalMovesList = self.pieceList
        for pieceName in legalMovesList['white'].items():
            for mailbox in pieceName[1]:
                for move, target in pieceName[1][mailbox].legalMoves:
                    self.board[target].watchedBy['white'].append(pieceName[1][mailbox])
        for pieceName in legalMovesList['black'].items():
            for mailbox in pieceName[1]:
                for move, target in pieceName[1][mailbox].legalMoves:
                    self.board[target].watchedBy['black'].append(pieceName[1][mailbox])
    
    def clearUnsafeKingSquares(self):
        next(iter((self.pieceList['white']['K'].items())))[1].cullUnsafeMoves(self.board)
        next(iter((self.pieceList['black']['K'].items())))[1].cullUnsafeMoves(self.board)
                                                                                # A bit of a ridiculous way to access the king in this particular structure: due to the fact that
                                                                                # dict.items() operates using views instead of lists, this is the fastest usage of iter and is thread-safe
                                                                                # See: https://blog.labix.org/2008/06/27/watch-out-for-listdictkeys-in-python-3 and
                                                                                # https://stackoverflow.com/questions/18552001/accessing-dict-keys-element-by-index-in-python3/27638751#27638751


    # Splits up FEN into sections for use in boardFromFen()
    @staticmethod
    def formatFEN(FEN):
        FEN = FEN.split("/")            # Splits FEN using slashes at first
        FENTip = FEN[7].split(' ')      # Additionally splits the ending by spaces
        FEN = FEN[:7] + FENTip          # Concatenates the slash split and space split arrays
        return FEN

    # Works its way DOWN the board form white's perspective (start rank 8, end rank 1) from left to right, adding appropriate piece from FEN as 
    # Designed in Forsyth-Edwards notation. See: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    def boardFromFEN(self, FEN):        
        self.clearBoard()
        FEN = self.formatFEN(FEN)
        print(FEN)                              # Can be taken out
        index = 0
        for section in FEN:
            if index < 8:
                target = 91 - (index * 10)      # FEN moves from top to bottom
                for piece in section:
                    try:
                        piece = int(piece)      # If value is empty space(s), move the target by that much
                        target += piece
                        continue
                    except Exception:
                        pass

                    if piece.islower():
                        self.addPiece(piece, 'black', target)
                        target += 1
                    else:
                        self.addPiece(piece, 'white', target)
                        target += 1
            elif index == 8:
                if FEN[7] == 'w':
                    self.playerTurnToPlay = 'white'
                else:
                    self.playerTurnToPlay = 'black'
            elif index == 9:
                castlingRights = FEN[8]                         # Optimized variable usage
                for letter in castlingRights:
                    if letter == '-':
                        pass
                    elif letter == 'K':
                        self.canCastle['white']['kingside'] = True      # Castling is handled in an orderly KQkq or - format in the FEN, see FEN notation reference
                    elif letter == 'Q':
                        self.canCastle['white']['queenside'] = True
                    elif letter == 'k':
                        self.canCastle['black']['kingside'] = True
                    elif letter == 'q':
                        self.canCastle['black']['kingside'] = True
            elif index == 10:
                self.enPassantSquare = FEN[9]
            elif index == 11:
                self.halfmoveClock = FEN[10]                            # Halfmove clock is number of halfmoves since last capture or pawn advance, can be used for draw under 50-move rule
            elif index == 12:
                self.currentTurn = FEN[11]
            index += 1
    
    def cullPins(self):
        pieceNames = ['B','Q','R']
        teamNames = ['white','black']
        for team in teamNames:
            for pieceName in pieceNames:
                for mailbox, piece in self.pieceList[team][pieceName].items():
                    for offset, xray in piece.xray.items():
                        if len(xray) < 2:
                            continue
                        pinTarget = xray[1]
                        pinnedPiece = xray[0]
                        inverseOffset = offset * (-1)
                        if (pinTarget.name == 'K') and (pinTarget.team != piece.team) and (pinnedPiece.team != piece.team):      # If king is enemy and being pinned with enemy piece
                            if (pinnedPiece.name != 'P') and (inverseOffset in pinnedPiece.offsets):                     # If piece is Bishop, Queen, or Rook (Not accounted for pawns yet)
                                newLegalMoves = []
                                target = pinnedPiece.mailbox + inverseOffset       
                                while ((self.board[target].mailbox > 0) and (self.board[target].piece is None)):        # This loop moves tile by tile, assessing the presence of a piece or out of bounds
                                    newLegalMoves.append(('move', target))                                              # If a piece is found, it attempts to see the pieces behind it, accounting for pins and xray attacks
                                    target += inverseOffset                                                             # Format for move storage: ('move'/'capture', mailbox of where move would put this piece)
                                if (self.board[target].piece is not None):
                                    if (self.board[target].piece.team != pinnedPiece.team):
                                        newLegalMoves.append(('capture', target))
                                pinnedPiece.legalMoves = newLegalMoves
                            else:
                                pinnedPiece.legalMoves = []
    
    # High-level function, coordinates board readiness of use for move pondering and other functions into one process.
    # TODO: Allow usage of commands in terminal to improve testing
    def initialize(self):
        self.generatePieceList()
        self.generateAllMoves()
        self.markBoardTiles()
        self.clearUnsafeKingSquares()
        self.cullPins()
        print("Board initialized")