from board import Board
from piece import *
from tile import Tile

chessBoard = Board("8/1kp5/8/3B4/4q3/3K4/8/8 w - -")
chessBoard.clearTile("D2")
chessBoard.refreshBoard()
chessBoard.display()
chessBoard.movePiece('E1','G1')
chessBoard.movePiece('E8','G8')
chessBoard.display()
print(chessBoard.nextMoves)
input() 
