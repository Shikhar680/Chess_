from start import Start
import pygame
from game import Game
from const import *
import sys,os

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Drag Chess")
        pygame_icon = pygame.image.load(os.path.join('chess_icon.png'))
        pygame.display.set_icon(pygame_icon)
        self.font = pygame.font.SysFont('monospace',18,bold=True)
        self.game = Game(3)

    def mainloop(self):
        game = self.game
        screen = self.screen
        
        color = "black"
        game.show_bg(screen)
        img = pygame.image.load(os.path.join('images.jpeg')).convert()
        img_rect = img.get_rect()
        img_rect.center = (WIDTH//2,(HEIGHT//2)-100)

        border_rect = (153,99,295,203)
        pygame.draw.rect(screen,"red",border_rect,width=10)
        
        label = self.font.render("Welcome to Chess!!! Press 1 to start",1,color)
        label1 = self.font.render("Note",1,color)
        label2 = self.font.render("Press 't' to change themes",1,color)
        label3 = self.font.render("Press 'r' to resign",1,color)
        label4 = self.font.render("Press 'q' to quit",1,color)
        label5 = self.font.render("Press 's' to restart",1,color)
        label_pos = label.get_rect()
        screen.blit(img, img_rect)
        label_pos.center = (WIDTH//2,(HEIGHT//2)+40)
        screen.blit(label,label_pos)
        label_pos1 = label1.get_rect()
        label_pos1.center = (WIDTH//2,(HEIGHT//2)+60)
        screen.blit(label1,label_pos1)
        label_pos2 = label2.get_rect()
        label_pos2.center = (WIDTH//2,(HEIGHT//2)+80)
        screen.blit(label2,label_pos2)
        label_pos3 = label3.get_rect()
        label_pos3.center = (WIDTH//2,(HEIGHT//2)+100)
        screen.blit(label3,label_pos3)
        label_pos4 = label4.get_rect()
        label_pos4.center = (WIDTH//2,(HEIGHT//2)+120)
        screen.blit(label4,label_pos4)
        label_pos5 = label5.get_rect()
        label_pos5.center = (WIDTH//2,(HEIGHT//2)+140)
        screen.blit(label5,label_pos5)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        m = Start(1)
                        m.mainloop()

                    if event.key == pygame.K_2:
                        m = Start(2)
                        m.mainloop()

                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                if (event.type == pygame.QUIT) :
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main = Main()
main.mainloop()