class Square:
    ALPHACOLS = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
    def __init__(self,r,c,p=None):  # r: row //// c: column ///// p: piece
        self.row=r
        self.col=c
        self.piece=p
        self.alphacols = self.ALPHACOLS[c]
    def __eq__(self,other):
        return (self.row == other.row) and (self.col == other.col)

    def has_piece(self):
        return self.piece != None
    
    def isEmpty(self):
        return not self.has_piece()
    def isRival(self,color):
        return self.has_piece() and self.piece.color!=color
    
    def isSameTeam(self,color):
        return self.has_piece() and self.piece.color==color

    def isEmptyOrRival(self,color):
        return self.isEmpty() or self.isRival(color)

    @staticmethod
    def in_range(*args):
        for a in args:
            if a<0 or a>7:
                return False
        return True
    
    def getAlphacol(col):
        ALPHACOLS = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
        return ALPHACOLS[col]
    