import copy
import math

def ucb(self, n=100):
    moves = self.legal_moves()
    sumScores = [0 for x in range (len(moves))]
    nbVisits = [0 for x in range (len(moves))]
    bestMoveIndex = 0
    
    # Simulations
    for i in range(n):
        bestScore = 0
        # Choose best move for current iteration
        for m in range(len(moves)):
            score = 1000000
            if nbVisits[m] > 0:
                score = sumScores[m] / nbVisits[m] + 0.4 * math.sqrt(math.log(i) / nbVisits[m])
            if score >= bestScore:
                bestScore = score
                bestMoveIndex = m
        # Playout for the current iteration        
        b = copy.deepcopy(self)
        b.play(moves[bestMoveIndex])
        r = b.playout()
        if self.turn == r:
            r = 1
        else:
            r = 0
        sumScores[bestMoveIndex] += r
        nbVisits[bestMoveIndex] += 1
        
    # Return best move from simulations
    bestScore = 0
    bestMoveIndex = 0
    for m in range(len(moves)):
        score = nbVisits[m]
        if score > bestScore:
            bestScore = score
            bestMoveIndex = m
            
    return moves[bestMoveIndex]