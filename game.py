from tile import Tile
from board import Board
from piece import *

chessBoard = Board()
chessBoard.makeBoard()
chessBoard.boardFromFEN("8/3k4/3qr3/8/1b1r2B1/2QR4/3K4/8 w - -")
chessBoard.clearTile("D2")
chessBoard.initialize()
chessBoard.display()
input() 
