from tile import Tile
from board import Board
from piece import *

chessBoard = Board()
chessBoard.makeBoard()
chessBoard.boardFromFEN("8/3k4/3qr3/8/1b1r2B1/2QR4/3K4/8 w - -")
chessBoard.initialize()
chessBoard.display()
print(chessBoard.board[43].piece.legalMoves)
print(chessBoard.board[44].piece.legalMoves)
print(chessBoard.board[52].piece.legalMoves)
print(chessBoard.board[54].piece.legalMoves)
print(chessBoard.board[57].piece.legalMoves)
print(chessBoard.board[74].piece.legalMoves)
print(chessBoard.board[75].piece.legalMoves)
print("King moves")
print(chessBoard.board[34].piece.legalMoves)
print(chessBoard.board[84].piece.legalMoves)
input() 
