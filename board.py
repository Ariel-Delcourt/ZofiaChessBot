from colorama import Back, Fore, init
from numpy import concatenate
from piece import *
from tile import Tile

init()

class Board:
    
    def __init__(self, FEN=None):
        self.board = []
        self.kingChecked = {'white': False, 'black': False}
        self.rookMoved = {'black': {'queenside': False, 'kingside': False}, 'white': {'queenside': False, 'kingside': False}}
        self.kingMoved = {'black': False, 'white': False}
        self.currentTurn = 0
        self.playerTurnToPlay = 'white'
        self.enPassantSquare = None
        self.pieceList = {
            'white': {'P': [], 'N': [], 'B': [], 'R': [], 'Q': [], 'K': []},
            'black': {'P': [], 'N': [], 'B': [], 'R': [], 'Q': [], 'K': []}
            }
        self.deadPieces = {
            'black': {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0},
            'white': {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0}
            }
        self.makeBoard()
        if FEN != None:
            self.boardFromFEN(FEN)
        
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
        print("Board cleared successfully.")

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
        self.currentTurn = 1
        self.playerTurnToPlay = 'white'


    def display(self):
        print()
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
            print("Successfully added", team,"Pawn to", Tile.mailboxToCoordinate(mailbox))
        elif (piece == 'R'):
            self.board[mailbox].piece = Rook(team, mailbox)
            print("Successfully added", team,"Rook to", Tile.mailboxToCoordinate(mailbox))
        elif (piece == 'N'):
            self.board[mailbox].piece = Knight(team, mailbox)
            print("Successfully added", team,"Knight to", Tile.mailboxToCoordinate(mailbox))
        elif (piece == 'B'):
            self.board[mailbox].piece = Bishop(team, mailbox)
            print("Successfully added", team,"Bishop to", Tile.mailboxToCoordinate(mailbox))
        elif (piece == 'Q'):
            self.board[mailbox].piece = Queen(team, mailbox)
            print("Successfully added", team,"Queen to", Tile.mailboxToCoordinate(mailbox))
        elif (piece == 'K'):
            self.board[mailbox].piece = King(team, mailbox)
            print("Successfully added", team,"King to", Tile.mailboxToCoordinate(mailbox))
        else:
            print("Incorrect piece code")

    def clearTile(self, coordinate):
        if type(coordinate) is str:
            mailbox = Tile.coordinateToMailbox(coordinate)
        self.board[mailbox].piece = None
        print("Tile", coordinate, "cleared successfully.")
    
    def generatePieceList(self):        # Generates multi-level dictionary containing objects of all pieces on the board
        self.pieceList = {
            'white': {'P': [], 'N': [], 'B': [], 'R': [], 'Q': [], 'K': []},
            'black': {'P': [], 'N': [], 'B': [], 'R': [], 'Q': [], 'K': []}
            }
        for tile in self.board:
            if (tile.piece is not None):
                self.pieceList[tile.piece.team][tile.piece.name].append(tile.piece)

    def sanityCheck(self):
        sanity = True
        if len(self.pieceList['white']['K']) < 1:
            print("Missing white king, cannot proceed.")
            sanity = False
        if len(self.pieceList['black']['K']) < 1:
            print("Missing black king, cannot proceed.")
            sanity = False
        return sanity
        

    def generateAllMoves(self):                              # Generates moves for all pieces on the board (stored in each piece's legalmoves dict)
        legalMovesList = self.pieceList                   # Does not account for pins, en passant, or castling
        for pieceName in legalMovesList['white'].items():
            for piece in pieceName[1]:
                piece.generateMoves(self.board)
        for pieceName in legalMovesList['black'].items():
            for piece in pieceName[1]:
                piece.generateMoves(self.board)

    def clearTileWatch(self):
        for tile in self.board:
            tile.watchedBy = {'white': [], 'black': []}


    def markBoardTiles(self):
        legalMovesList = self.pieceList
        for pieceName in legalMovesList['white'].items():
            for piece in pieceName[1]:    
                for origin, move, target in piece.listAllLegalMoves():
                    self.board[target].watchedBy['white'].append(piece)
        for pieceName in legalMovesList['black'].items():
            for piece in pieceName[1]: 
                for origin, move, target in piece.listAllLegalMoves():
                    self.board[target].watchedBy['black'].append(piece)
    
    def clearUnsafeKingSquares(self):
        self.pieceList['white']['K'][0].cullUnsafeMoves(self.board)
        self.pieceList['black']['K'][0].cullUnsafeMoves(self.board)

    '''
    King must not have moved
    King must not be in check
    Castling rook must not have moved
    Any squares the King passes through or into must:
        Not be watched by any opposing piece
        Not contain any other pieces
    '''
    def generateCastleMoves(self):
        if (not (self.kingChecked['white']) and not (self.kingMoved['white'])):
            king = self.pieceList['white']['K'][0]
            if (not (self.rookMoved['white']['queenside']) and (len(self.board[24].watchedBy['black']) == 0) and (len(self.board[23].watchedBy['black']) == 0)):
                if (self.board[24].piece is None) and (self.board[23].piece is None) and (self.board[22].piece is None):
                    king.legalMoves.append((king.mailbox, 'castle', 23))
            if (not (self.rookMoved['white']['kingside']) and (len(self.board[26].watchedBy['black']) == 0) and (len(self.board[27].watchedBy['black']) == 0)):
                if (self.board[26].piece is None) and (self.board[27].piece is None):
                    self.pieceList['white']['K'][0].legalMoves.append((king.mailbox, 'castle', 27))

        if (not (self.kingChecked['black']) and not (self.kingMoved['black'])):
            king = self.pieceList['black']['K'][0]
            if (not (self.rookMoved['black']['queenside']) and (len(self.board[94].watchedBy['white']) == 0) and (len(self.board[93].watchedBy['white']) == 0)):
                if (self.board[94].piece is None) and (self.board[93].piece is None) and (self.board[92].piece is None):
                    king.legalMoves.append((king.mailbox, 'castle', 93))
            if (not (self.rookMoved['black']['kingside']) and (len(self.board[96].watchedBy['white']) == 0) and (len(self.board[97].watchedBy['white']) == 0)):
                if (self.board[96].piece is None) and (self.board[97].piece is None):
                    king.legalMoves.append((king.mailbox, 'castle', 97))
    
    def generateEnPassantMoves(self):
        destination = self.enPassantSquare
        if destination == '-':
            return
        capturingTeam = None
        referenceTile = None
        if destination > 50:                                    # If the en passant square from the FEN is a lower mailbox than 50, then it is an en passant move for black pawns
            referenceTile = destination - 10
            capturingTeam = 'white'
        else:
            referenceTile = destination + 10
            capturingTeam = 'black'
        if self.board[referenceTile + 1].piece is not None:
            pawn = self.board[referenceTile + 1].piece
            if (pawn.name == 'P') and (pawn.piece.team == capturingTeam):           # If there are pawns on the capturing team to give en passant legality to... do so
                pawn.legalMoves.append((pawn.mailbox, 'enPassant', destination))
        if self.board[referenceTile - 1].piece is not None:
            pawn = self.board[referenceTile - 1].piece
            if (pawn.name == 'P') and (pawn.team == capturingTeam):
                pawn.legalMoves.append((pawn.mailbox, 'enPassant', destination))
    
    def areKingsChecked(self):
        if (len(self.board[self.pieceList['black']['K'][0].mailbox].watchedBy['white']) > 0):
            self.kingChecked['black'] = True
        else:
            self.kingChecked['black'] = False
        
        if (len(self.board[self.pieceList['white']['K'][0].mailbox].watchedBy['black']) > 0):
            self.kingChecked['white'] = True
        else:
            self.kingChecked['white'] = False

    # Specify location of piece to be moved and location of its destination, removes piece from current tile and replaces the piece at its destination
    # Grants en passant to neighboring pawns after a pawn double move if they exist
    # Handles castling move logic
    # Handles en passant move logic
    # Returns true if move was legal, false otherwise
    def movePiece(self, mailbox, destination):
        mailbox = Tile.coordinateToMailbox(mailbox)
        destination = Tile.coordinateToMailbox(destination)
        movingPiece = self.board[mailbox].piece
        if movingPiece is None:
            print('Illegal Move, chosen tile is empty')
            return False
        targetPiece = self.board[destination].piece
        for (origin, moveType, target) in movingPiece.legalMoves:
            if destination == target:
                movingPiece.mailbox = destination

                if moveType == 'move':
                    self.board[destination].piece = movingPiece
                    self.board[mailbox].piece = None
                
                elif moveType == 'doubleMove':
                    self.board[destination].piece = movingPiece
                    self.board[mailbox].piece = None
                    if movingPiece.team == 'white':
                        self.enPassantSquare = destination - 10
                    else:
                        self.enPassantSquare = destination + 10
                    self.generateEnPassantMoves()
                
                elif moveType == 'capture':
                    self.deadPieces[targetPiece.team][targetPiece.name] += 1
                    self.board[destination].piece = movingPiece
                    self.board[mailbox].piece = None
                    self.pieceList[targetPiece.team][targetPiece.name]
                
                elif moveType == 'castle':
                    if movingPiece.team == 'white':
                        if destination == 23:
                            targetRook = self.board[21].piece
                            targetRook.mailbox = 23
                            self.board[destination].piece = movingPiece
                            self.board[mailbox].piece = None
                            self.board[23].piece = targetRook
                            self.board[21].piece = None
                        elif destination == 27:
                            targetRook = self.board[28].piece
                            targetRook.mailbox = 25
                            self.board[destination].piece = movingPiece
                            self.board[mailbox].piece = None
                            self.board[25].piece = targetRook
                            self.board[28].piece = None

                    elif movingPiece.team == 'black':
                        if destination == 93:
                            targetRook = self.board[91].piece
                            targetRook.mailbox = 93
                            self.board[destination].piece = movingPiece
                            self.board[mailbox].piece = None
                            self.board[93].piece = targetRook
                            self.board[91].piece = None
                        elif destination == 97:
                            targetRook = self.board[98].piece
                            targetRook.mailbox = 95
                            self.board[destination].piece = movingPiece
                            self.board[mailbox].piece = None
                            self.board[95].piece = targetRook
                            self.board[98].piece = None
                            
                elif moveType == 'enPassant':
                    if movingPiece.team == 'white':                                         # If a white pawn en passant captures a black one
                        targetPiece = self.board[destination - 10].piece
                        self.board[destination].piece = movingPiece
                        self.board[mailbox].piece = None
                        self.board[destination - 10].piece = None
                        self.deadPieces[targetPiece.team][targetPiece.name] += 1

                    elif movingPiece.team == 'black':                                         # If a black pawn en passant captures a white one
                        targetPiece = self.board[destination + 10].piece
                        self.board[destination].piece = movingPiece
                        self.board[mailbox].piece = None
                        self.board[destination + 10].piece = None
                        self.deadPieces[targetPiece.team][targetPiece.name] += 1

                return True                                                                 # True for success, false for failure
        print('Illegal Move')
        return False

    # Splits up FEN into sections for use in boardFromFen()
    @staticmethod
    def formatFEN(FEN):
        FEN = FEN.split("/")            # Splits FEN using slashes at first
        FENTip = FEN[7].split(' ')      # Additionally splits the ending by spaces
        FEN = FEN[:7] + FENTip          # Concatenates the slash split and space split arrays
        return FEN

    def removeKingCheckedMoves(self, king, checkingPieces):
        for checkingPiece in checkingPieces:
            offsets = checkingPiece.offsets
            vector = king.mailbox - checkingPiece.mailbox
            selectedOffset = -float('inf')
            for offset in offsets:
                if (vector // offset > 0) and (vector % offset == 0) and (abs(offset) > selectedOffset):
                    selectedOffset = offset
            king.legalMoves[selectedOffset] = []
            king.legalMoves[-selectedOffset] = []

    # Calculates blocking moves, killing moves, and escape moves respectively
    # Must be run after all pins have been culled and safe king squares evaluated.
    def cullCheckMoves(self):
        finalMoves = []
        if self.playerTurnToPlay == 'white':
            king = self.pieceList['white']['K'][0]
            self.removeKingCheckedMoves(king, self.board[king.mailbox].watchedBy['black'])
            if len(self.board[king.mailbox].watchedBy['black']) > 1:
                return king.listAllLegalMoves()
            else:
                checkingPiece = self.board[king.mailbox].watchedBy['black'][0]
                for piece in self.board[checkingPiece.mailbox].watchedBy['white']:
                    if piece.name != 'K':
                        finalMoves.append((piece.mailbox, 'capture',checkingPiece.mailbox))
                if (checkingPiece.name == 'P') or (checkingPiece.name == 'N'):
                    return finalMoves
                else:
                    finalMoves += self.findBlockingMoves(king, checkingPiece)

        elif self.playerTurnToPlay == 'black':
            king = self.pieceList['black']['K'][0]
            self.removeKingCheckedMoves(king, self.board[king.mailbox].watchedBy['white'])
            if len(self.board[king.mailbox].watchedBy['white']) > 1:
                return king.listAllLegalMoves()
            else:
                checkingPiece = self.board[king.mailbox].watchedBy['white'][0]
                for piece in self.board[checkingPiece.mailbox].watchedBy['black']:
                    if piece.name != 'K':
                        finalMoves.append((piece.mailbox, 'capture',checkingPiece.mailbox))
                if (checkingPiece.name == 'P') or (checkingPiece.name == 'N'):
                    return finalMoves
                else:
                    finalMoves += self.findBlockingMoves(king, checkingPiece)
        finalMoves += king.listAllLegalMoves()
        return finalMoves
                
    def findBlockingMoves(self, targetKing, checkingPiece):
        offsets = checkingPiece.offsets
        vector = targetKing.mailbox - checkingPiece.mailbox
        selectedOffset = -float('inf')
        blockingMoves = []
        for offset in offsets:
            if (vector // offset > 0) and (vector % offset == 0) and (abs(offset) > selectedOffset):
                selectedOffset = offset
        targetMailbox = targetKing.mailbox - selectedOffset
        while self.board[targetMailbox].piece is None:
            possiblePieces = self.board[targetMailbox].watchedBy[targetKing.team]
            if len(possiblePieces) > 0:
                for piece in possiblePieces:
                    if piece.name != 'K':
                        blockingMoves.append((piece.mailbox, 'block', targetMailbox))
            targetMailbox -= selectedOffset
        return blockingMoves

    # Works its way DOWN the board form white's perspective (start rank 8, end rank 1) from left to right, adding appropriate piece from FEN as 
    # Designed in Forsyth-Edwards notation. See: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    def boardFromFEN(self, FEN):        
        self.clearBoard()
        FEN = self.formatFEN(FEN)
        print(FEN)
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
                if FEN[8] == 'w':
                    self.playerTurnToPlay = 'white'
                else:
                    self.playerTurnToPlay = 'black'
            elif index == 9:
                castlingRights = FEN[9]                         # Optimized variable usage
                for letter in castlingRights:
                    if letter == '-':
                        self.kingMoved['white'] = True
                        self.kingMoved['black'] = True
                    elif letter == 'K':
                        self.rookMoved['white']['kingside'] = False      # Castling is handled in an orderly KQkq or - format in the FEN, see FEN notation reference
                    elif letter == 'Q':                                 # Here the rooks being moved might be a false statement depending on the board state, 
                        self.rookMoved['white']['queenside'] = False     # but it simplifies the meaning and results in an equivalent board state 
                    elif letter == 'k':
                        self.rookMoved['black']['kingside'] = False
                    elif letter == 'q':
                        self.rookMoved['black']['kingside'] = False
            elif index == 10:
                if FEN[10] == '-':
                     self.enPassantSquare = '-'
                else:
                    self.enPassantSquare = Tile.coordinateToMailbox(FEN[10])
            elif index == 11:
                self.halfmoveClock = FEN[11]                            # Halfmove clock is number of halfmoves since last capture or pawn advance, can be used for draw under 50-move rule
            elif index == 12:
                self.currentTurn = FEN[12]
            index += 1
    
    def cullPins(self):
        pieceNames = ['B','Q','R','P','N']
        teamNames = ['white','black']
        for team in teamNames:
            for pieceName in pieceNames:
                for piece in self.pieceList[team][pieceName]:
                    for offset, xray in piece.xray.items():
                        if len(xray) < 2:
                            continue
                        pinTarget = xray[1]
                        pinnedPiece = xray[0]
                        inverseOffset = offset * (-1)
                        if (pinTarget.name == 'K') and (pinTarget.team != piece.team) and (pinnedPiece.team != piece.team):      # If king is enemy and being pinned with enemy piece
                            pinnedPiece.legalMoves = {pinnedPiece.legalMoves[inverseOffset]}                                     # Piece can therefore only move along the pinned vector

    def listAllTeamMoves(self, team):
        teamMoves = []
        for pieceType in self.pieceList[team].items():
            for piece in pieceType[1]:
                teamMoves += piece.listAllLegalMoves()
        return teamMoves

    def refreshBoard(self):
        self.generatePieceList()
        self.generateAllMoves()
        self.clearTileWatch()
        self.markBoardTiles()
        self.clearUnsafeKingSquares()
        self.generateEnPassantMoves()
        self.cullPins()
        self.areKingsChecked()
        self.generateCastleMoves()
        self.cullCheckMoves()
        self.nextMoves = self.listAllTeamMoves(self.playerTurnToPlay)
