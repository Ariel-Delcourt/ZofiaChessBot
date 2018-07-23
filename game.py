from tile import Tile
from board import Board
from piece import *

chessBoard = Board()
chessBoard.makeBoard()
chessBoard.boardFromFEN("r1b1kb1r/ppp1qppp/2np1n2/4p3/2B1P3/2PP1N2/PP3PPP/RNBQ1RK1 b kq - 0 6")
chessBoard.generatePieceList()
chessBoard.generateAllMoves()
chessBoard.display()
print(chessBoard.board[91].piece.xray)
input() 
