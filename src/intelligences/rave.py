import copy
import math
from src.common.constants import RED,MAX_LEGAL_MOVES, MAX_PLAYOUT_LEGAL_MOVES


def update_transposition_table_amaf(transpositionT, h, nb_playouts, trys, wins, trys_inPlayout, wins_inPlayout):
    if h in transpositionT:
        transpositionT[h]["total_playouts"] += nb_playouts
        for key, value in zip(
            ["trys_per_move", "wins_per_move", "trys_inPlayout_per_move", "wins_inPlayout_per_move"], 
            [trys, wins, trys_inPlayout, wins_inPlayout]
        ):
            transpositionT[h][key] = [i+j for i,j in zip(transpositionT[h][key], value)]
    else:        
        transpositionT[h] = {
            "total_playouts": nb_playouts, 
            "trys_per_move": trys, 
            "wins_per_move": wins,
            "trys_inPlayout_per_move": trys_inPlayout, 
            "wins_inPlayout_per_move": wins_inPlayout
        }

def rave_search(self, n, transpositionT):
    #self.transposition_table[self.turn] = {}
    for i in range(n):
        b1 = copy.deepcopy(self)
        res = self._RAVE(b1, [], transpositionT)
    elt_state = transpositionT[self.hash]
    moves = self.legal_moves()
    best_move = moves[0]
    best_value = elt_state["trys_per_move"][0]
    for i in range(1, len(moves)):
        if elt_state["trys_per_move"][i] > best_value:
            best_value = elt_state["trys_per_move"][i]
            best_move = moves[i]
    return best_move


def _RAVE(self, board, played, transpositionT):
    color = board.turn
    moves = board.legal_moves()
    tokens_level = board.tokens_level
    if board.finished:
        return board.winner
    running_hash = board.hash
    if running_hash in transpositionT:
        elt_state = transpositionT[running_hash]
        best_value = float("-inf")
        best_move = 0
        total_playouts = elt_state["total_playouts"]
        for m in range(0, len(moves)): 
            value = float("inf")
            code = moves[m].code_AMAF(tokens_level)
            trys = elt_state["trys_per_move"][m]
            wins = elt_state["wins_per_move"][m]
            amaf_visits = elt_state["trys_inPlayout_per_move"][code]
            amaf_scores = elt_state["wins_inPlayout_per_move"][code]
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
        res = self._RAVE(board, played, transpositionT)
        trys = [0.0 if i != best_move else 1 for i in range(MAX_LEGAL_MOVES)]
        won = 1 if RED == res else 0
        wins = [0.0 if i != best_move else won for i in range(MAX_LEGAL_MOVES)]
        amaf_visits = [0.0 if k!=moves[best_move].code_AMAF(tokens_level) else 1 for k in range(MAX_PLAYOUT_LEGAL_MOVES)]
        amaf_scores = [0.0 if k!=moves[best_move].code_AMAF(tokens_level) else won for k in range(MAX_PLAYOUT_LEGAL_MOVES)]
        for i in range(len(played)):
            code = played[i].code_AMAF(tokens_level)
            seen = False
            for j in range(i):
                if played[j].code_AMAF(tokens_level)==code:
                    seen = True
            if not seen:
                amaf_visits = [el if k != code else 1 for k, el in enumerate(amaf_visits)]
                amaf_scores = [el if k != code else won for k, el in enumerate(amaf_scores)]

        update_transposition_table_amaf(transpositionT, running_hash, 1, trys, wins, amaf_visits, amaf_scores)
        played.insert(0, moves[best_move])
        return res
    else:
        trys = [0.0 for i in range(MAX_LEGAL_MOVES)]
        wins = [0.0 for i in range(MAX_LEGAL_MOVES)]
        amaf_visits = [0.0 for i in range(MAX_PLAYOUT_LEGAL_MOVES)]
        amaf_scores = [0.0 for i in range(MAX_PLAYOUT_LEGAL_MOVES)]
        update_transposition_table_amaf(transpositionT, running_hash, 1, trys, wins, amaf_visits, amaf_scores)

        res = board.playout(played=played)

        return res