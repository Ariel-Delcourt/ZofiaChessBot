from tile import Tile
from board import Board
from piece import *

class Game:

    def __init__(self):
        chessBoard = Board()
        currentTurn = 'white'       #can be white or black
        turnNumber = 0
        
