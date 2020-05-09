import copy
def flat_mc(self, n=1000):
        moves = self.legal_moves()
        scores = []
        nb_ite_per_move = int(n/len(moves))
        for move in moves:
            total = 0
            for i in range(nb_ite_per_move):
                copy_board = copy.deepcopy(self)
                copy_board.play(move)
                won = 1 if copy_board.playout() == self.turn else 0
                total += won
            scores.append(total)
        return moves[scores.index(max(scores))]