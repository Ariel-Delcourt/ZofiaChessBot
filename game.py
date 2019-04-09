from board import Board
from piece import *
from tile import Tile


class Game:

    def __init__(self, FEN=None):
        self.chessBoard = Board(FEN)
        self.chessBoard.refreshBoard()
