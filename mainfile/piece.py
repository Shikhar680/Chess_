import os
class Piece:
    def __init__(self, name, color, value, play_as,texture=None, texture_rect=None):
        self.name=name
        self.color=color
        if play_as == 1:
            value_sign = 1 if color=='white' else -1
        elif play_as == 2:
            value_sign = -1 if color=='white' else 1
        self.value = value * value_sign
        self.texture = texture
        # self.tot_moves = []
        self.moves = []
        self.captures = []
        self.moved = False
        self.set_texture()
        self.texture_rect = texture_rect
    
    def set_texture(self,size=80):
        # if size==60:
        self.texture = os.path.join(f'pieceimg/img{size}/{self.color}__{self.name}.png')
        # else:
        #     self.texture = os.path.join(f'pieceimg/{self.color}-{self.name}.png')
    
    def add_move(self,move):
        self.moves.append(move)

    def add_capture(self,capture):
        self.captures.append(capture)

    def clear_moves(self):
        self.moves = []
        self.captures = []

class Pawn(Piece):
    def __init__(self, color, play_as):
        super().__init__('pawn', color, 1.0, play_as)
        self.en_passant = False
        self.movee = 0
        if play_as == 1:
            self.dir = -1 if color=='white' else 1
        elif play_as == 2:
            self.dir = 1 if color=='white' else -1

class Knight(Piece):
    def __init__(self, color, play_as):
        super().__init__('knight', color, 3.0, play_as)
        
class Bishop(Piece):
    def __init__(self, color, play_as):
        super().__init__('bishop', color, 3.0, play_as)
        
class Rook(Piece):
    def __init__(self, color, play_as):
        super().__init__('rook', color, 5.0, play_as)

class Queen(Piece):
    def __init__(self, color, play_as):
        super().__init__('queen', color, 9.0, play_as)

class King(Piece):
    def __init__(self, color, play_as):
        self.left_rook = None
        self.right_rook = None
        self.check = False
        super().__init__('king', color, 10000.0, play_as)

    