import copy
import math
from src.common.constants import RED,MAX_LEGAL_MOVES, MAX_PLAYOUT_LEGAL_MOVES

# AMAF Transposition table (a bouger dans une classe Player ou TranspositionTable) 
def _update_transposition_table_amaf(transpositionTable, h, nb_playouts, trys, wins, trys_inPlayout, wins_inPlayout):
    if h in transpositionTable:
        transpositionTable[h]["total_playouts"] += nb_playouts
        for key, value in zip(
            ["trys_per_move", "wins_per_move", "trys_inPlayout_per_move", "wins_inPlayout_per_move"], 
            [trys, wins, trys_inPlayout, wins_inPlayout]
        ):
            transpositionTable[h][key] = [i+j for i,j in zip(transpositionTable[h][key], value)]
    else:        
        transpositionTable[h] = {
            "total_playouts": nb_playouts, 
            "trys_per_move": trys, 
            "wins_per_move": wins,
            "trys_inPlayout_per_move": trys_inPlayout, 
            "wins_inPlayout_per_move": wins_inPlayout
        }
            
def _GRAVE(board, played, tref, transpositionTable):    
    # On se place du pt de vue de RED pour les stats (winner)
    
    #print("State: " + str(board.hashState)) 
    
    # SI TERMINAL
    if(board.finished):
        #print("Terminal node")
        r = board.winner
        if r != RED:
            r = 0
        return r
    
    # SI NOEUD CONNU
    t = transpositionTable.get(board.hash)
    if t != None:
        
        # Si le noeud a été joué > 50 fois : cas RAVE classique.
        # Sinon t est égal à tref (i.e. le dernier noeud joué > 50 fois)
        tr = tref
        if t["total_playouts"] > 50:
            tr = t
        
        # Initialisation pour comparaison
        bestValue = -1000000.0
        best = 0
        moves = board.legal_moves()
        #print("Nb legal moves: " + str(len(moves)))
        # On identifie le meilleur move en utilisant les statistiques AMAF
        for i in range(len(moves)):
            val = 1000000.0
            code = moves[i].code_AMAF()
            
            # Si le coup a déjà été joué au cours d'un playout depuis cet état, on calcule sa valeur
            if t["trys_inPlayout_per_move"][code] > 0:
                #print("Move "+str(i)+ " has already been played in AMAF stats for real board state " + str(board.hashState) )
                beta = t["trys_inPlayout_per_move"][code] / (t["trys_per_move"][i] + t["trys_inPlayout_per_move"][code] + 1e-5 * t["trys_per_move"][i] * t["trys_inPlayout_per_move"][code])
                Q = 1
                if t["trys_per_move"][i] > 0:
                    Q = t["wins_per_move"][i] / t["trys_per_move"][i]
                    if board.turn != RED:
                        Q = 1 - Q
                AMAF = t["wins_inPlayout_per_move"][code] / t["trys_inPlayout_per_move"][code]
                if board.turn != RED:
                    AMAF = 1 - AMAF
                val = (1.0 - beta) * Q + beta * AMAF
            #print("Val for move " + str(i) + ": " + str(val))
            # On prend le coup à la valeur max   
            if val >= bestValue:
                bestValue = val
                best = i
                
        # On update les statistiques classique de ce coup qui sera joué en début de playout
        #print("Transition table in state " + str(board.hashState)+ ": " +str(t))
        #print("Move "+ str(best) + " is played in playout begining in state " + str(board.hashState))
        
        #print("Stats in state " + str(board.hashState) + " are now (visits): " + str(t))
       
        # On joue le meilleur coup
        b_simulation = copy.deepcopy(board)
        b_simulation.play(moves[best])
        
        #print("Simulated board state: " + str(b_simulation.hashState))
        #print("- Recursive call -")
        
        res = _GRAVE(b_simulation, played, tr, transpositionTable) # Appel récursif pour suivre GRAVE jusqu'à un noeud terminal / une nouvelle feuille
        #if board.turn == res:
         #   r = 1
        #else:
            #r = 0
        t["total_playouts"] += 1
        t["trys_per_move"][best] += 1
        t["wins_per_move"][best] += res
        
        #print("Stats in state "+ str(board.hashState) + " are now (result): " +str(t))
        #print("-- Break full simulation --")
        
        # On update les statistiques AMAF de tous les coups joués en cours de playout
        #print(str(len(played)) + " played moves during playout")
        for i in range(len(played)):
            code = played[i].code_AMAF()
            seen = False
            for j in range(i):
                if played[j].code_AMAF() == code:
                    seen = True
            # On MAJ uniquement la première fois qu'on a joué le coup durant le playout
            if not seen:
                t["trys_inPlayout_per_move"][code] += 1
                t["wins_inPlayout_per_move"][code] += res
                
        #print("Stats AMAF updatées")
        
        #print("Stats in state "+ str(board.hashState) + " are now (AMAF): " +str(t))
        # On rajoute dans l'arbre le coup qu'on a joué (pour que la liste historise chaque appel récursif)
        # Ainsi, au noeud terminal on peut utiliser les liste played pour MAJ les statistiques AMAF avec tous les coups du playout 
        played.insert(0, moves[best])
        
        return res
    
    # SI FEUILLE À CRÉER
    else:
        trys = [0.0 for i in range(MAX_LEGAL_MOVES)]
        wins = [0.0 for i in range(MAX_LEGAL_MOVES)]
        trys_inPlayout = [0.0 for i in range(MAX_PLAYOUT_LEGAL_MOVES)]
        wins_inPlayout = [0.0 for i in range(MAX_PLAYOUT_LEGAL_MOVES)]
        _update_transposition_table_amaf(transpositionTable, board.hash, 1, trys, wins, trys_inPlayout, wins_inPlayout)         
                
        #print("Leaf added for state " + str(board.hashState))
        #print("Stats for state " + str(board.hashState) + ": " + str(lookUpState(transpositionTable, board)))
        
        result = board.playout_AMAF(played)
        if result != RED:
            result = 0
        
        #print("Result of playout: " + str(result))
        #print("- Break recursive call -")
        
        return result
    
def grave_search(self, nb_iterations, transpositionTable):
    
    # On effectue les simulations avec RAVE
    for i in range(nb_iterations):
        t = transpositionTable.get(self.hash)
        b = copy.deepcopy(self)
        res = _GRAVE(b, [], t, transpositionTable) # On passe une liste vide au départ pour indiquer qu'il n'y a pas d'historique de playout
    #print(transpositionTable)
    t = transpositionTable.get(self.hash)
    moves = self.legal_moves()
    best = moves[0]
    bestValue = t["trys_per_move"][0]
    
    # On choisit le move le plus simulé
    for i in range (1, len(moves)):
        if (t["trys_per_move"][i] > bestValue):
            bestValue = t["trys_per_move"][i]
            best = moves[i]
    return best