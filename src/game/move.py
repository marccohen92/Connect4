from src.common.constants import DY, RED


class Move():
    
    def __init__(self, color, column):
        self.color = color
        self.column = column
        
    def render(self):
        template = "color : {}, column: {}."
        print(template.format(self.color, self.column))
        
        
    def equals(self, otherMove):
        if (otherMove.color == self.color) & (otherMove.column == self.column) :
            return True
        else:
            return False
        
    # On veut coder (comme un hash) chacun des 5*5*3 coups possibles * 2 couleurs
    def code_AMAF(self):
        # Encode 2 colors * DY columns possible moves
        if self.color == RED :
            code = self.column
        else : 
            code = (self.column + 1) * (DY + 1)
        return code
        