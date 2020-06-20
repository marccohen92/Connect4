import copy
import math
from src.common.constants import RED,MAX_LEGAL_MOVES, MAX_PLAYOUT_LEGAL_MOVES


def grave_search_bis(self, n=1000, threshold=50):
    #self.transposition_table[self.turn] = {}
    for i in range(n):
        b1 = copy.deepcopy(self)
        if b1.hash in b1.transposition_table[self.turn - 1]:
            elt_ref = b1.transposition_table[self.turn - 1][b1.hash]
        else:
            elt_ref=None
        res = self._GRAVE_BIS(b1, [], elt_ref, threshold)
    elt_state = self.transposition_table[self.turn - 1][self.hash]
    moves = self.legal_moves()
    best_move = moves[0]
    best_value = elt_state["trys_per_move"][0]
    for i in range(1, len(moves)):
        if elt_state["trys_per_move"][i] > best_value:
            best_value = elt_state["trys_per_move"][i]
            best_move = moves[i]
    return best_move


def _GRAVE_BIS(self, board, played, elt_ref, threshold=50):
    color = board.turn
    moves = board.legal_moves()
    if board.finished:
        return board.winner
    running_hash = board.hash
    if running_hash in self.transposition_table[color - 1]:
        elt_state = self.transposition_table[color - 1][running_hash]
        elt_r = elt_ref
        total_playouts = elt_state["total_playouts"]
        if total_playouts > threshold:
            elt_r = elt_state
        best_value = float("-inf")
        best_move = 0
        for m in range(0, len(moves)): 
            value = float("inf")
            code = moves[m].code_AMAF()
            trys = elt_state["trys_per_move"][m]
            wins = elt_state["wins_per_move"][m]
            amaf_visits = elt_r["trys_inPlayout_per_move"][code]
            amaf_scores = elt_r["wins_inPlayout_per_move"][code]
            if amaf_visits > 0:
                beta = amaf_visits / (trys + amaf_visits + 1e-5 * trys * amaf_visits)
                Q = 1
                if trys > 0:
                    Q = wins/ trys
                    if board.turn != RED:
                        Q = 1-Q
                AMAF = amaf_scores/amaf_visits
                if board.turn != RED:
                        AMAF = 1-AMAF
                value = (1.0-beta)*Q+beta*AMAF

            if value > best_value:
                best_value = value
                best_move = m


        board.play(moves[best_move])
        res = self._GRAVE_BIS(board, played, elt_r, threshold)
        trys = [0.0 if i != best_move else 1 for i in range(MAX_LEGAL_MOVES)]
        won = 1 if RED == res else 0
        wins = [0.0 if i != best_move else won for i in range(MAX_LEGAL_MOVES)]
        amaf_visits = [0.0 if k!=moves[best_move].code_AMAF() else 1 for k in range(MAX_PLAYOUT_LEGAL_MOVES)]
        amaf_scores = [0.0 if k!=moves[best_move].code_AMAF() else won for k in range(MAX_PLAYOUT_LEGAL_MOVES)]
        for i in range(len(played)):
            code = played[i].code_AMAF()
            seen = False
            for j in range(i):
                if played[j].code_AMAF()==code:
                    seen = True
            if not seen:
                amaf_visits = [el if k != code else 1 for k, el in enumerate(amaf_visits)]
                amaf_scores = [el if k != code else won for k, el in enumerate(amaf_scores)]

        self._update_transposition_table_amaf(running_hash, 1, trys, wins, amaf_visits, amaf_scores)
        played.insert(0, moves[best_move])
        return res
    else:
        trys = [0.0 for i in range(MAX_LEGAL_MOVES)]
        wins = [0.0 for i in range(MAX_LEGAL_MOVES)]
        amaf_visits = [0.0 for i in range(MAX_PLAYOUT_LEGAL_MOVES)]
        amaf_scores = [0.0 for i in range(MAX_PLAYOUT_LEGAL_MOVES)]
        self._update_transposition_table_amaf(running_hash, 1, trys, wins, amaf_visits, amaf_scores)

        res = board.playout(played=played)

        return res