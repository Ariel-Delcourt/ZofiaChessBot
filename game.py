from board import Board
from piece import *
from tile import Tile


class Game:

    def __init__(self, name, FEN=None):
        self.chessBoard = Board(FEN)
        self.chessBoard.refreshBoard()
        self.name = name

    def startGame(self):
        self.chessBoard.display()
        while len(self.chessBoard.nextMoves) > 0:
            print("Turn", self.chessBoard.currentTurn, ":",self.chessBoard.playerTurnToPlay, "to play.")
            validInput = False
            while not validInput:
                request = input()
                if request[0] == '/':
                    request = request[1:]
                    self.parseCommand(request)
                    continue
                request = Game.parseMoveRequest(request)
                if self.chessBoard.movePiece(request[0], request[1]):
                    validInput = True
            self.chessBoard.nextTurn()
            self.chessBoard.display()

        if self.chessBoard.kingChecked[self.chessBoard.playerTurnToPlay]:
            print("Checkmate on", self.chessBoard.playerTurnToPlay + ".")
            input()
        else:
            print("Draw, no moves for", self.chessBoard.playerTurnToPlay + ".")
            input()
                
    def parseCommand(self, command):
        if command == 'moves':
            print(self.chessBoard.nextMoves)


    @staticmethod
    def parseMoveRequest(request):
        request = request.split(' ')
        request = [Tile.coordinateToMailbox(x) for x in request]
        return request
