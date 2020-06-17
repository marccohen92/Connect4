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

def fight_bis(p1, p2, nb_playouts=1000, verbose=False, p1_transpositionTable={}, first_turn=0):
    board = Board()
    if first_turn % 2:
        board.turn = RED
    else:
        board.turn = YELLOW
    while(not board.finished):
        if verbose:
            print(board.board)
            print("Turn "+str(board.turn))
        if board.turn == RED:
            # RED (player 1) plays RAVE with AMAF transposition table
            move = getattr(board, p1)(nb_playouts, p1_transpositionTable)
        elif board.turn == YELLOW:
            move = getattr(board, p2)(nb_playouts)
        board.play(move)
    if verbose:
        print(board.board)
    return board.winner

def fight_bis_bis(p1, p2, nb_playouts=1000, verbose=False, p1_transpositionTable={}, p2_transpositionTable={}, first_turn=0):
    board = Board()
    if first_turn % 2:
        board.turn = RED
    else:
        board.turn = YELLOW
    while(not board.finished):
        if verbose:
            print(board.board)
            print("Turn "+str(board.turn))
        if board.turn == RED:
            # RED (player 1) plays RAVE with AMAF transposition table
            move = getattr(board, p1)(nb_playouts, p1_transpositionTable)
        elif board.turn == YELLOW:
            move = getattr(board, p2)(nb_playouts, p2_transpositionTable)
        board.play(move)
    if verbose:
        print(board.board)
    return board.winner