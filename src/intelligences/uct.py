import copy
import math
from src.common.constants import MAX_LEGAL_MOVES

def update_transposition_table(transpositionT, h, nb_playouts, trys, wins):
    if h in transpositionT:
        transpositionT[h]["total_playouts"] += nb_playouts
        for key, value in zip(["trys_per_move", "wins_per_move"], [trys, wins]):
            transpositionT[h][key] = [i+j for i,j in zip(transpositionT[h][key], value)]
    else:
        transpositionT[h] = {"total_playouts": nb_playouts, "trys_per_move": trys, "wins_per_move": wins}


def uct_search(self, n, transpositionT):
    #self.transposition_table = [{}, {}]
    # Commentée pour conserver la même transposition_table au cours d'un fight
    
    # For debug:
    #elt_prev = self.transposition_table[self.turn - 1].get(self.hash)
    #print("Stats for state ", self.hash, ": ", elt_prev)
    
    for i in range(n) :
        #print()
        #print("========== ", i)
        #print("========== ", i)
        #print("========== ", i)
        #print()
        copyBoard = copy.deepcopy(self)
        self._uct(copyBoard, transpositionT)
        
    elt_state = transpositionT[self.hash]
    #print("Stats for state ", self.hash, ": ", elt_state)
    
    moves = self.legal_moves()
    best_move = moves[0]
    best_index = 0
    best_value = elt_state["trys_per_move"][0]
    for i in range(1, len(moves)):
        if elt_state["trys_per_move"][i] > best_value:
            best_value = elt_state["trys_per_move"][i]
            best_move = moves[i]
            best_index = i
    #print("best_index: ", best_index)
    return best_move


def _uct(self, board, transpositionT):
    #print("=== _UCT CALL")
    #print("State: ", board.hash)
    color = board.turn
    #print("Color to play: ", color)
    moves = board.legal_moves()
    #print("Nb legal moves : ", len(moves))
    #print("Legal moves :")
    #for move in moves:
        #print("Color: ", move.color)
        #print("Column: ", move.column)
    
    if board.finished:
        #print(" -> Terminal state")
        return board.winner

    running_hash = board.hash
    #print("Board current hash: ", running_hash)
    
    if running_hash in transpositionT:
        #print(" -> Known state")
        elt_state = transpositionT[running_hash]
        #print("State stats: ", elt_state)
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
        #print("Best move index to play: ", best_move)
        res = 0.0
        if (len(moves) > 0):
            
            trys = [0.0 if i != best_move else 1 for i in range(MAX_LEGAL_MOVES)]
            
            board.play(moves[best_move])
            
            #print("=== Start recursive call...")
            res = self._uct(board, transpositionT)
            #print("=== ... End recursive call, result was ", res)
            
            won = 1 if res == color else 0
            wins = [0.0 if i != best_move else won for i in range(MAX_LEGAL_MOVES)]
            
            
            update_transposition_table(transpositionT, running_hash, 1, trys, wins)
            #print("Updated transposition table for hash ", running_hash)
            #print(self.transposition_table[self.turn-1][running_hash])

        return res
    else:
        #print(" -> Unknown state")
        trys = [0.0 for i in range(MAX_LEGAL_MOVES)]
        wins = [0.0 for i in range(MAX_LEGAL_MOVES)]
        update_transposition_table(transpositionT, running_hash, 1, trys, wins) 
        #print("Updated transposition table for hash ", running_hash)
        #print(self.transposition_table[self.turn-1][running_hash])
        res = board.playout()

        return res
    