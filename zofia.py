from tile import Tile
from board import Board
from piece import *

chessBoard = Board()
chessBoard.makeBoard()
chessBoard.boardFromFEN("r4rk1/pp3ppp/1n6/2qp4/6b1/2PQ1N2/P3BPPP/R3R1K1 w - -")
chessBoard.clearTile("D2")
chessBoard.initialize()
chessBoard.display()
chessBoard.movePiece('G4','F3')
chessBoard.display()
input() 
