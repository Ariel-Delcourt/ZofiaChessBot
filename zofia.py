from board import Board
from piece import *
from tile import Tile

chessBoard = Board()
chessBoard.makeBoard()
chessBoard.boardFromFEN("r2qk2r/8/8/8/2Pp4/8/8/R3K2R b KQkq c3")
chessBoard.clearTile("D2")
chessBoard.initialize()
chessBoard.display()
print(chessBoard.pieceList['black']['K'][0].legalMoves)
chessBoard.movePiece('E1','G1')
chessBoard.movePiece('E8','G8')
chessBoard.display()
print(chessBoard.pieceList['black']['P'][0].legalMoves)
print(chessBoard.pieceList['white']['K'][0].legalMoves)
input() 
