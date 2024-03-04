import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
class Game:
    def __init__(self,play_as):
        self.next_player = "white"
        self.board = Board(play_as)
        self.dragger = Dragger()
        self.config = Config()
        self.move_c = 1
        self.play_as = play_as
        
    def show_bg(self,surface):
        theme = self.config.theme
        for r in range(rows):
            for c in range(cols):
                color = theme.bg.light if (r+c)%2 == 0 else theme.bg.dark
                sq = (c*sq_size,r*sq_size,sq_size,sq_size)
                pygame.draw.rect(surface, color, sq)

    def show_labels(self,surface):
        theme = self.config.theme
        for r in range(rows):
            for c in range(cols):
                if self.play_as == 1:
                    if c == 0:
                        color = theme.bg.dark if r%2 == 0 else theme.bg.light
                        label = self.config.font.render(str(rows-r),1,color)
                        label_pos = (5,5 + r*sq_size)
                        surface.blit(label,label_pos)
                    if r == 0:
                        color = theme.bg.light if c%2 == 0 else theme.bg.dark
                        label = self.config.font.render(Square.getAlphacol(c),1,color)  #str(chr(105-(cols-c)))
                        label_pos = (sq_size-20+ c*sq_size,HEIGHT-20)
                        surface.blit(label,label_pos)

                if self.play_as == 2:
                    if c == 0:
                        color = theme.bg.dark if r%2 == 0 else theme.bg.light
                        label = self.config.font.render(str(9-(rows-r)),1,color)
                        label_pos = (5,5 + r*sq_size)
                        surface.blit(label,label_pos)
                    if r == 0:
                        color = theme.bg.light if c%2 == 0 else theme.bg.dark
                        label = self.config.font.render(Square.getAlphacol(7-c),1,color)  #str(chr(105-(cols-c)))
                        label_pos = (sq_size-20+ c*sq_size,HEIGHT-20)
                        surface.blit(label,label_pos)
    
    def show_pieces(self,surface):
        for r in range(rows):
            for c in range(cols):
                if self.board.squares[r][c].has_piece():
                    piece = self.board.squares[r][c].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(60)
                        img = pygame.image.load(piece.texture)
                        img_center = c*sq_size+sq_size//2,r*sq_size+sq_size//2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img,piece.texture_rect)
    
    def showMoves(self,surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                cen = (move.final.col*sq_size+sq_size//2,move.final.row*sq_size+sq_size//2)
                color =  theme.moves.light if (move.final.row + move.final.col)%2==0 else theme.moves.dark
                pygame.draw.circle(surface,color,cen,circ_rad//4)

            for capture in piece.captures:
                color = theme.moves.light if (capture.final.row + capture.final.col) % 2==0 else theme.moves.dark
                rect = (capture.final.col*sq_size+sq_size//2,capture.final.row*sq_size+sq_size//2)
                pygame.draw.circle(surface,color,rect,circ_rad,width=6)

    def showLastMove(self,surface):
        theme = self.config.theme
        if self.board.lastmove:
            initial = self.board.lastmove.initial
            final = self.board.lastmove.final
            for pos in [initial,final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col*sq_size,pos.row*sq_size,sq_size,sq_size)
                pygame.draw.rect(surface,color,rect)

    def showcurrplace(self,surface):
        clicked_row = self.dragger.mouseY//sq_size
        clicked_col = self.dragger.mouseX//sq_size
        rect = (clicked_col*sq_size,clicked_row*sq_size,sq_size,sq_size)
        color = "#F4F680" if (clicked_row+clicked_col)%2==0 else "#BBCC44"
        pygame.draw.rect(surface,(234,235,232),rect,width=4)

    def next_turn(self):
        if self.next_player == "black":
            self.next_player = "white"
            self.move_c += 1
        else:
            self.next_player = "black"
    
    def changeTheme(self):
        self.config.changeTheme()

    def sound_effect(self,check=False,promote=False,castle=False,capture=False):
        if check:
            return
        elif promote:
            self.config.promote_sound.play()
        elif castle:
            self.config.castle_sound.play()
        elif capture:
            self.config.capture_sound.play()
        else: self.config.move_sound.play()
        
    def reset(self,play_as):
        print("*"*50,"\nGame Restart\n","*"*50)
        self.__init__(play_as)
        self.next_player = "white"
        self.board = Board(play_as)
        self.dragger = Dragger()
        self.config = Config()
        self.move_c = 1