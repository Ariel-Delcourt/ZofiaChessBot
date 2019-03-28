from board import Board
from piece import *
from tile import Tile


class Game:

    def __init__(self):
        chessBoard = Board()
        currentTurn = 'white'       #can be white or black
        turnNumber = 0
