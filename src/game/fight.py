from src.game.board import Board
from src.common.constants import RED, YELLOW


def fight(p1, p1_table, p2, p2_table, nb_playouts=1000, verbose=True):
    board = Board()
    if p1_table:
        transpositionT1 = {}
    if p2_table:
        transpositionT2 = {}
    while(not board.finished):
        if verbose:
            print(board.board)
            print("Turn "+str(board.turn))
            
        if board.turn == RED:
            if p1_table:
                move = getattr(board, p1)(nb_playouts, transpositionT1)
            else :
                move = getattr(board, p1)(nb_playouts)
        elif board.turn == YELLOW:
            if p2_table:
                move = getattr(board, p2)(nb_playouts, transpositionT2)
            else :
                move = getattr(board, p2)(nb_playouts)
            
        board.play(move)
    if verbose:
        print(board.board)
        print("Winner :" + int(board.winner))
    return board.winner
