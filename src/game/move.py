from src.common.constants import DX, DY, RED


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
        
    def code_AMAF(self, tokens_level):
        if self.color == RED :
            #code = self.column + tokens_level[self.column] * DY 
            code = self.column
        else : 
            #code = self.column + tokens_level[self.column] * DY + (DY + DX * DY)
            code = self.column + DY
        return code
        