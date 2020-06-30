import copy
import math
from src.common.constants import MAX_LEGAL_MOVES

def uct_search(self, n=1000):
    #self.transposition_table = [{}, {}]
    # Commentée pour conserver la même transposition_table au cours d'un fight
    for i in range(n) :
        copyBoard = copy.deepcopy(self)
        self._uct(copyBoard)
    elt_state = self.transposition_table[self.turn - 1][self.hash]
    moves = self.legal_moves()
    best_move = moves[0]
    best_value = elt_state["trys_per_move"][0]
    for i in range(1, len(moves)):
        if elt_state["trys_per_move"][i] > best_value:
            best_value = elt_state["trys_per_move"][i]
            best_move = moves[i]
    return best_move


def _uct(self, board):
    color = board.turn
    moves = board.legal_moves()
    if board.finished:
        return board.winner

    running_hash = board.hash
    if running_hash in self.transposition_table[color-1]:
        elt_state = self.transposition_table[color-1][running_hash]
        best_value = float("inf")
        best_move = 0
        total_playouts = elt_state["total_playouts"]
        if elt_state["trys_per_move"][0] > 0:
            trys = elt_state["trys_per_move"][0]
            wins = elt_state["wins_per_move"][0]
            best_value = wins / trys + 0.4 * math.sqrt(math.log(total_playouts) / trys)
        for m in range(1, len(moves)):                
            trys = elt_state["trys_per_move"][m]
            wins = elt_state["wins_per_move"][m]
            value = float("inf")
            if trys > 0:
                value = wins / trys + 0.4 * math.sqrt(math.log(total_playouts) / trys)
            if value > best_value:
                best_value = value
                best_move = m
        res = 0.0
        if (len(moves) > 0):
            board.play(moves[best_move])
            res = self._uct(board)
            trys = [0.0 if i != best_move else 1 for i in range(MAX_LEGAL_MOVES)]
            won = 1 if res == color else 0
            wins = [0.0 if i != best_move else won for i in range(MAX_LEGAL_MOVES)]
            self._update_transposition_table(running_hash, 1, trys, wins)

        return res
    else:
        trys = [0.0 for i in range(MAX_LEGAL_MOVES)]
        wins = [0.0 for i in range(MAX_LEGAL_MOVES)]
        self._update_transposition_table(running_hash, 1, trys, wins) 

        res = board.playout()

        return res
    