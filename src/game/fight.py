from src.game.board import Board
from src.common.constants import RED, YELLOW

def fight(p1, p2, nb_playouts=1000, verbose=True):
    board = Board()
    while(not board.finished):
        if verbose:
            print(board.board)
            print("Turn "+str(board.turn))
        if board.turn == RED:
            move = getattr(board, p1)(nb_playouts)
        elif board.turn == YELLOW:
            move = getattr(board, p2)(nb_playouts)
        board.play(move)
    if verbose:
        print(board.board)
    return board.winner

def fight_transpositionT(p1, p1_table, p2, p2_table, nb_playouts=1000, verbose=True):
    board = Board()
    if p1_table:
        transpositionT1 = {}
    if p2_table:
        transpositionT2 = {}
    while(not board.finished):
        if verbose:
            print(board.board)
            print("Turn "+str(board.turn))
            
        if p1_table and p2_table:
            if board.turn == RED:
                move = getattr(board, p1)(nb_playouts, transpositionT1)
            elif board.turn == YELLOW:
                move = getattr(board, p2)(nb_playouts, transpositionT2)
                
        elif p1_table and not p2_table:
            if board.turn == RED:
                move = getattr(board, p1)(nb_playouts, transpositionT1)
            elif board.turn == YELLOW:
                move = getattr(board, p2)(nb_playouts)
                
        elif not p1_table and p2_table:
            if board.turn == RED:
                move = getattr(board, p1)(nb_playouts)
            elif board.turn == YELLOW:
                move = getattr(board, p2)(nb_playouts, transpositionT2)
                
        elif not p1_table and not p2_table:
            if board.turn == RED:
                move = getattr(board, p1)(nb_playouts)
            elif board.turn == YELLOW:
                move = getattr(board, p2)(nb_playouts)
            
        board.play(move)
    if verbose:
        print(board.board)
    return board.winner
