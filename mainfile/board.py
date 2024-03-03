from const import *
from square import Square
from piece import *
from move import Move
import pygame
import copy
import os
from sound import Sound

class Board:
    def __init__(self,play_as):
        self.squares = [[0]*8 for col in range(cols)]
        self._create()
        if play_as == 1:
            self._addpieces_white('white')
            self._addpieces_white('black')
        elif play_as == 2:
            self._addpieces_black('white')
            self._addpieces_black('black')
        self.lastmove = None
        self.play_as = play_as

    def _create(self):
        for r in range(rows):
            for c in range(cols):
                self.squares[r][c] = Square(r,c)

    def ac_move(self,piece,move, testing = False):
        initial = move.initial
        final = move.final
        diff = final.col - initial.col

        en_passant_empty = self.squares[final.row][final.col].isEmpty()

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece=piece

        if isinstance(piece, Pawn):
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col+diff].piece = None
                self.squares[final.row][final.col].piece=piece
                if not testing:
                    sound = Sound(os.path.join('sounds/capture.mp3'))
                    sound.play()
            else:
                self.check_promotion(piece,final)

        if isinstance(piece,King):
            if self.castling(initial,final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff<0) else piece.right_rook
                if rook.moves != []:
                    self.ac_move(rook,rook.moves[-1])
        if self.lastmove:
            self.en_passant_false(self.lastmove)
        piece.moved = True
        piece.clear_moves()
        self.lastmove = move        
    
    def validate_move(self,piece,move):
        return move in (piece.moves + piece.captures)

    def check_promotion(self,piece,final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color,self.play_as)
            
    def castling(self,initial,final):
        return abs(initial.col - final.col) == 2

    def in_check(self,piece,move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.ac_move(temp_piece,move,testing=True)

        for ro in range(rows):
            for co in range(cols):
                if temp_board.squares[ro][co].isRival(piece.color):
                    p = temp_board.squares[ro][co].piece
                    temp_board.calcmoves(p, ro, co, bool=False)
                    for m in p.captures:
                        if isinstance(m.final.piece,King):
                            return True
        return False
    
    def calcmoves(self,piece,row,col,bool=True):
        valid_moves = []

        def knight_moves():
            possible_moves=[(row-2, col-1), (row-2, col+1), (row-1, col-2), (row-1, col+2), (row+1, col-2),
                             (row+1, col+2), (row+2, col-1), (row+2, col+1)]
            for pm in possible_moves:
                pm_row,pm_col = pm
                if Square.in_range(pm_row,pm_col):
                     if self.squares[pm_row][pm_col].isEmptyOrRival(piece.color):
                         initial = Square(row,col)
                         f_piece = self.squares[pm_row][pm_col].piece
                         final = Square(pm_row,pm_col,f_piece)                             
                         move=Move(initial,final)
                         if self.squares[pm_row][pm_col].isRival(piece.color):
                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_capture(move)
                            else:
                                piece.add_capture(move)
                         else:
                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

        def stlinesmoves(moveset):
            for direction in moveset:
                row_in, col_in = direction
                pm_row, pm_col = row + row_in, col + col_in
                while Square.in_range(pm_row, pm_col):
                    initial = Square(row, col)
                    
                    f_piece = self.squares[pm_row][pm_col].piece
                    final = Square(pm_row, pm_col,f_piece)
                    move = Move(initial, final)
                    if self.squares[pm_row][pm_col].isEmpty():
                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        
                    elif self.squares[pm_row][pm_col].isRival(piece.color):
                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_capture(move)
                        else:
                            piece.add_capture(move)
                        break
                    else:
                        break
                    pm_row += row_in
                    pm_col += col_in

        def king_moves():
            possible_moves = [(row+1,col), (row,col+1), (row,col-1), (row-1,col), (row+1,col+1), (row-1,col-1), (row+1,col-1), (row-1,col+1)]
            for pm in possible_moves:
                pm_row,pm_col = pm
                if Square.in_range(pm_row,pm_col):
                    if self.squares[pm_row][pm_col].isEmptyOrRival(piece.color):
                        initial = Square(row,col)
                        final = Square(pm_row,pm_col)
                        move=Move(initial,final)
                        if self.squares[pm_row][pm_col].isRival(piece.color): 
                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_capture(move)
                            else:
                                piece.add_capture(move)
                        else:
                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)


            castle_lking_final,castle_rking_final,castle_lrook_final,castle_rrook_final,castle_lcheck_range,castle_rcheck_range,e_point = (2,6,3,5,range(1,4),range(5,7),3) if self.play_as == 1 else (1,5,2,4,range(1,3),range(4,7),2)
            if not piece.moved:
                if not piece.check:
                    left_rook = self.squares[row][0].piece
                    if isinstance(left_rook,Rook):
                        if not left_rook.moved:
                            for c in castle_lcheck_range:
                                if self.squares[row][c].has_piece():break
                                if c == e_point:
                                    piece.left_rook = left_rook
                                    initial = Square(row,0)
                                    final = Square(row,castle_lrook_final)
                                    move = Move(initial,final)
                                    if bool:
                                        if not self.in_check(left_rook,move):
                                            left_rook.add_move(move)
                                    else:
                                        left_rook.add_move(move)
                                    

                                    initial = Square(row,col)
                                    final = Square(row,castle_lking_final)
                                    move = Move(initial,final)
                                    if bool:
                                        if not self.in_check(piece,move):
                                            piece.add_move(move)
                                    else:
                                        piece.add_move(move)

                    right_rook = self.squares[row][7].piece
                    if isinstance(right_rook,Rook):
                        if not right_rook.moved:
                            for c in castle_rcheck_range:
                                if self.squares[row][c].has_piece():break
                                if c == 6:
                                    piece.right_rook = right_rook

                                    initial = Square(row,7)
                                    final = Square(row,castle_rrook_final)
                                    move = Move(initial,final)
                                    if bool:
                                        if not self.in_check(right_rook,move):
                                            right_rook.add_move(move)
                                    else:
                                        right_rook.add_move(move)

                                    initial = Square(row,col)
                                    final = Square(row,castle_rking_final)
                                    move = Move(initial,final)
                                    if bool:
                                        if not self.in_check(piece,move):
                                            piece.add_move(move)
                                    else:
                                        piece.add_move(move)
                    
        def pawn_moves(piece):
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * ( 1 + steps))
            for move_row in range(start,end,piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isEmpty():
                        initial = Square(row,col)
                        final = Square(move_row,col)
                        move = Move(initial,final)
                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else: break
                else: break

            if self.play_as == 1:
                r = 3 if piece.color == "white" else 4
                f_r = 2 if piece.color == "white" else 5
            elif self.play_as == 2:
                r = 4 if piece.color == "white" else 3
                f_r = 5 if piece.color == "white" else 2
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].isRival(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row,col)
                            
                            final = Square(f_r,col-1,p)
                            capture = Move(initial,final)
                            if bool:
                                if not self.in_check(piece,capture):
                                    piece.add_capture(capture)
                            else:
                                piece.add_capture(capture)

            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].isRival(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row,col)
                            
                            final = Square(f_r,col+1,p)
                            capture = Move(initial,final)
                            if bool:
                                if not self.in_check(piece,capture):
                                    piece.add_capture(capture)
                            else:
                                piece.add_capture(capture)

            pm_row = row + piece.dir
            pm_cols = [col-1,col+1]
            for pm_col in pm_cols:
                if Square.in_range(pm_row,pm_col): 
                    if self.squares[pm_row][pm_col].isRival(piece.color):
                        initial = Square(row,col)
                        f_piece = self.squares[pm_row][pm_col].piece
                        final = Square(pm_row,pm_col,f_piece)
                        capture = Move(initial,final)
                        if bool:
                            if not self.in_check(piece,capture):
                                piece.add_capture(capture)
                        else:
                            piece.add_capture(capture)   

        if isinstance(piece, Pawn):
            pawn_moves(piece)
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            stlinesmoves([(1,1),(1,-1),(-1,-1),(-1,1)])
        elif isinstance(piece, Rook):
            stlinesmoves([(0,1),(1,0),(0,-1),(-1,0)])
        elif isinstance(piece, Queen):
            stlinesmoves([
                (1,1),(1,-1),(-1,-1),(-1,1),
                (0,1),(1,0),(0,-1),(-1,0)
            ])
        elif isinstance(piece, King):
            king_moves()

        valid_moves = piece.moves+piece.captures
        return valid_moves

    def _addpieces_black(self,color):
        row_pawn,row_other = (1,0) if color=='white' else (6,7)

        for col in range(cols):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color,2))

        self.squares[row_other][1] = Square(row_other,1,Knight(color,2))
        self.squares[row_other][6] = Square(row_other,6,Knight(color,2))

        self.squares[row_other][2] = Square(row_other,2,Bishop(color,2))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color,2))

        self.squares[row_other][0] = Square(row_other,0,Rook(color,2))
        self.squares[row_other][7] = Square(row_other,7,Rook(color,2))

        self.squares[row_other][3] = Square(row_other,3,King(color,2))
        self.squares[row_other][4] = Square(row_other,4,Queen(color,2))

    def _addpieces_white(self,color):
        row_pawn,row_other = (6,7) if color=='white' else (1,0)

        for col in range(cols):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color,1))

        self.squares[row_other][1] = Square(row_other,1,Knight(color,1))
        self.squares[row_other][6] = Square(row_other,6,Knight(color,1))

        self.squares[row_other][2] = Square(row_other,2,Bishop(color,1))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color,1))

        self.squares[row_other][0] = Square(row_other,0,Rook(color,1))
        self.squares[row_other][7] = Square(row_other,7,Rook(color,1))

        self.squares[row_other][4] = Square(row_other,4,King(color,1))
        self.squares[row_other][3] = Square(row_other,3,Queen(color,1))

    def asc_move(self,piece,move,p_as):
        f = 0
        final=move.final
        initial = move.initial
        a = ""
        if self.squares[final.row][final.col].has_piece():
            if isinstance(piece,Pawn):
                if final.row == 0 or final.row == 7:
                    f = 1
                if p_as == 1:
                    a += chr(move.initial.col+97)
                elif p_as == 2:
                    a += chr((7-move.initial.col)+97)
            a += "x"
        else: a += ""
        if p_as == 1:
            m = name_d[piece.name] + a + chr(move.final.col+97) + str(8 - move.final.row)
        elif p_as == 2:
            m = name_d[piece.name] + a + chr((7-move.final.col)+97) + str(move.final.row+1)
        if f==1:
            m += "=Q"
        return m
        
    def ischeck(self,piece,pos):
        row,col = pos
        p_move = self.calcmoves(piece,row,col)
        c = False
        if self.curr_move_check(p_move,piece.color):
            c = True
        return c
    
    def curr_move_check(self,moves,color):
        for i in moves:
            if isinstance(self.squares[i.final.row][i.final.col].piece,King):
                if self.squares[i.final.row][i.final.col].isRival(color):
                    return True
        return False
    
    def king_in_check(self,color):
        temp_board = copy.deepcopy(self)
        for r in range(rows):
            for c in range(cols):
                if temp_board.squares[r][c].isRival(color):
                    p = temp_board.squares[r][c].piece
                    m = temp_board.calcmoves(p,r,c,bool=False)
                    for i in m:
                        if isinstance(temp_board.squares[i.final.row][i.final.col].piece,King):
                            return True
        return False

    def valid_options_move(self,color):
        temp_board = copy.deepcopy(self)
        for r in range(rows):
            for c in range(cols):
                if temp_board.squares[r][c].isSameTeam(color):
                    p = temp_board.squares[r][c].piece
                    m = temp_board.calcmoves(p,r,c,bool=True)
                    for i in m:
                        if i:
                            return True
        return False
                        
    def checkmate(self,color):
        if not self.valid_options_move(color):
            if self.king_in_check(color):
                print("Checkmate")
                return 1
            else:
                print("Stalemate")
                return 2
        return
    
    def is_en_passant(self,piece,move):
        if isinstance(piece,Pawn):
            if abs(move.initial.row - move.final.row) == 2:
                piece.en_passant = True
                return True
        return False
    
    def en_passant_false(self,lastmove):
        if isinstance(self.squares[lastmove.final.row][lastmove.final.col].piece,Pawn):
            self.squares[lastmove.final.row][lastmove.final.col].piece.en_passant = False

    def set_king_check(self,np):
        if self.king_in_check(np):
            for ro in range(rows):
                for col in range(cols):
                    if self.squares[ro][col].isSameTeam(np):
                        if isinstance(self.squares[ro][col].piece,King):
                            self.squares[ro][col].piece.check = True
        else:
            for ro in range(rows):
                for col in range(cols):
                    if self.squares[ro][col].isSameTeam(np):
                        if isinstance(self.squares[ro][col].piece,King):
                            self.squares[ro][col].piece.check = False

    def check_draw(self):
        white_pieces = []
        black_pieces = []
        for r in range(rows):
            for c in range(cols):
                if self.squares[r][c].has_piece():
                    if self.squares[r][c].piece.color == "white":
                        white_pieces.append(self.squares[r][c].piece.name)
                    if self.squares[r][c].piece.color == "black":
                        black_pieces.append(self.squares[r][c].piece.name)
        
        needed_pieces = ["queen","pawn","rook"]
        a = 0
        for i in needed_pieces:
            if (i not in white_pieces) and (i not in black_pieces):
                a+=1
        if a == 3:
            if white_pieces.count('bishop')<2 or white_pieces.count('knight')<2:
                if black_pieces.count('bishop')<2 or black_pieces.count('knight')<2:
                    print("Draw")