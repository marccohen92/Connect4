import copy
import math
def ucb(self, nb_playouts=1000):
    moves = self.legal_moves()
    trys_list = [1 for i in range(len(moves))]
    wins_list = [0 for i in range(len(moves))]
    scores = [1000000 for i in range(len(moves))]
    for i in range(nb_playouts):
        running_move_idx = scores.index(max(scores))
        move = moves[running_move_idx]
        copy_board = copy.deepcopy(self)
        copy_board.play(move)
        won = 1 if copy_board.playout() == self.turn else 0
        wins_list[running_move_idx] = wins_list[running_move_idx] + won
        trys_list[running_move_idx] = trys_list[running_move_idx] + 1
        for m in range(len(moves)):
            scores[m] = wins_list[m] / trys_list[m] + 0.4 * math.sqrt(math.log(i+1) / trys_list[m])
    return moves[scores.index(max(scores))]