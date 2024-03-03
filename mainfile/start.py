import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move
from piece import *

class Start:
    def __init__(self,play_as):
        pygame.init()
        self.font = pygame.font.SysFont('monospace',18,bold=True)
        self.font1 = pygame.font.SysFont('monospace',30,bold=True)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.game = Game(play_as)
        self.play_as=play_as

    def mainloop(self):
        game,screen,dragger,board=self.game,self.screen,self.game.dragger,self.game.board
        f = 0
        while True:
            game.show_bg(screen)
            game.showLastMove(screen)
            game.show_labels(screen)
            game.showMoves(screen)
            if dragger.dragging:
                game.showcurrplace(screen)
            game.show_pieces(screen)
            if dragger.dragging:
                dragger.update_blit(screen)
                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_t:
                        game.changeTheme()

                    if event.key == pygame.K_s:
                        print("Reset")
                        game.reset(self.play_as)
                        f=0
                        game,dragger,board=self.game,self.game.dragger,self.game.board

                    if event.key == pygame.K_q:
                        print("Thanks for playing!!")
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_r:
                        print("\n",game.next_player.upper(),"Resigns")
                        move_made = game.move_c
                        if game.next_player == "white":
                            result =  "0 - 1"
                            winner = "black"
                            move_made -= 1

                        else: 
                            result = "1 - 0"
                            winner = "white"
                        print("*"*50,"\nCONGRATULATIONS!!! ",winner.upper(),"WINS \nWIN BY RESIGNATION\n","Moves made:",move_made,"\nResult: ",result,"\n","*"*50)
                        pygame.quit()
                        sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                   dragger.updatemouse(event.pos)
                   clicked_row = dragger.mouseY//sq_size
                   clicked_col = dragger.mouseX//sq_size
                   if board.squares[clicked_row][clicked_col].has_piece():
                       piece = board.squares[clicked_row][clicked_col].piece
                       if piece.color == game.next_player:
                            board.calcmoves(piece,clicked_row,clicked_col,bool=True)
                            
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            if dragger.dragging:
                                game.showcurrplace(screen)
                            game.show_bg(screen)
                            game.showLastMove(screen)
                            game.show_labels(screen)
                            game.showMoves(screen)
                            game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.updatemouse(event.pos)
                        game.show_bg(screen)
                        game.showLastMove(screen)
                        game.show_labels(screen)
                        game.showMoves(screen)
                        game.showcurrplace(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    x,y = event.pos

                    if Square.in_range(x//sq_size,y//sq_size):
                        if board.squares[y//sq_size][x//sq_size].has_piece():
                            board.squares[y//sq_size][x//sq_size].piece.clear_moves()

                    else:
                        if dragger.dragging:
                            dragger.undrag_piece()
                    
                    if dragger.dragging:
                        dragger.updatemouse(event.pos)
                        released_row = dragger.mouseY//sq_size
                        released_col = dragger.mouseX//sq_size
                        initial = Square(dragger.initial_row,dragger.initial_col)
                        final = Square(released_row,released_col)        
                        check1 = board.ischeck(dragger.piece,(released_row,released_col))

                        move = Move(initial,final)
                        if board.validate_move(dragger.piece, move):

                            capture1 = board.squares[released_row][released_col].has_piece()
                            game.sound_effect(capture=capture1,check=check1)
                            if dragger.piece.color=="white":
                                print(game.move_c,end=". ")
                                moveprint = board.asc_move(dragger.piece,move,self.play_as)
                                if check1 == True:
                                    moveprint+="+"
                                print(moveprint,end=" ")

                            else:
                                moveprint = board.asc_move(dragger.piece,move,self.play_as)
                                if check1 == True:
                                    moveprint+="+"
                                print(moveprint)

                            board.ac_move(dragger.piece,move)
                            board.is_en_passant(dragger.piece,move)
                            game.show_bg(screen)
                            game.showLastMove(screen)
                            game.show_labels(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                            board.set_king_check(game.next_player)
                            board.check_draw()
                            if board.checkmate(game.next_player)==1:
                                f=1
                                move_made = game.move_c
                                wcolor = game.next_player
                                if wcolor == "white":
                                    wcolor = "black"
                                    result =  "0 - 1"
                                    move_made-=1
                                else: 
                                    wcolor = "white"
                                    result = "1 - 0"
                                print("*"*50,"\nCONGRATULATIONS!!! ",wcolor.upper(),"WINS \nCHECKMATE \n","Moves made:",move_made,"\nResult: ",result,"\n","*"*50)                           
                                self.end_screen(screen,move_made,wcolor,result)
                            
                        else:
                            dragger.piece.clear_moves()
                    dragger.undrag_piece()
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if f==1:
                self.end_screen(screen,move_made,wcolor,result)
            pygame.display.update()

    def end_screen(self,screen,move_count,pcolor,result):
            color = "white"
            rect = (sq_size,sq_size*2,sq_size*6,sq_size*4)
            pygame.draw.rect(screen,color,rect)
            pygame.draw.rect(screen,"red",(sq_size-10,(sq_size*2)-10,(sq_size*6)+20,(sq_size*4)+20),width=10)
            t_color = "black"
            label = self.font1.render("CHECKMATE!!!",1,t_color)
            label1 = self.font1.render(f"{pcolor.upper()} WINS",1,t_color)
            label2 = self.font1.render(f"Moves made: {move_count}",1,t_color)
            label3 = self.font1.render(f"Result: {result}",1,t_color)
            label_pos = label.get_rect()
            label_pos.center = (WIDTH//2,HEIGHT//2-30)
            screen.blit(label,label_pos)
            label_pos1 = label1.get_rect()
            label_pos1.center = (WIDTH//2,HEIGHT//2)
            screen.blit(label1,label_pos1)
            label_pos2 = label2.get_rect()
            label_pos2.center = (WIDTH//2,(HEIGHT//2)+30)
            screen.blit(label2,label_pos2)
            label_pos3 = label3.get_rect()
            label_pos3.center = (WIDTH//2,(HEIGHT//2)+60)
            screen.blit(label3,label_pos3)
