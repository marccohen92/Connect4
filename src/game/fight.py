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
