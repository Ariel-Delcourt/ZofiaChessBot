from tile import Tile
from piece import *
from colorama import Fore, Back, init
init()

class Board:
    
    def __init__(self):
        self.board = []
        
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

    def addPiece(self, piece, team, coordinate):
        piece = str.capitalize(piece)
        team = str.lower(team)
        mailbox = Tile.coordinateToMailbox(coordinate)
        if (piece == 'P'):
            self.board[mailbox].piece = Pawn(team, mailbox)
            print("Successfully added", team,"Pawn to", coordinate)
        elif (piece == 'R'):
            self.board[mailbox].piece = Rook(team, mailbox)
            print("Successfully added", team,"Rook to", coordinate)
        elif (piece == 'N'):
            self.board[mailbox].piece = Knight(team, mailbox)
            print("Successfully added", team,"Knight to", coordinate)
        elif (piece == 'B'):
            self.board[mailbox].piece = Bishop(team, mailbox)
            print("Successfully added", team,"Bishop to", coordinate)
        elif (piece == 'Q'):
            self.board[mailbox].piece = Queen(team, mailbox)
            print("Successfully added", team,"Queen to", coordinate)
        elif (piece == 'K'):
            self.board[mailbox].piece = King(team, mailbox)
            print("Successfully added", team,"King to", coordinate)
        else:
            print("Incorrect piece code")
    
    def generatePieceList(self):
        pieceList = {
            'white': {'P': {}, 'N': {}, 'B': {}, 'R': {}, 'Q': {}, 'K': {}},
            'black': {'P': {}, 'N': {}, 'B': {}, 'R': {}, 'Q': {}, 'K': {}}
            }
        
        for tile in self.board:
            if (tile.piece is not None):
                pieceList[tile.piece.team][tile.piece.name][tile.piece.mailbox] = tile.piece
        self.pieceList = pieceList

    def generateMoves(self):
        legalMovesList = self.pieceList                   #Does not account for pins, en passant, or castling
        for pieceName in legalMovesList['white'].items():
            for mailbox in pieceName[1]:
                pieceName[1][mailbox].generateMoves(self.board)
        for pieceName in legalMovesList['black'].items():
            for mailbox in pieceName[1]:
                pieceName[1][mailbox].generateMoves(self.board)