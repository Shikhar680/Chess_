import pygame
import os
from sound import Sound
from theme import Theme
class Config:
    def __init__(self):
        self.themes = []
        self.addThemes()
        self.idx = 0
        self.theme = self.themes[self.idx]

        self.font = pygame.font.SysFont('monospace',18,bold=True)
        self.move_sound = Sound(
            os.path.join('sounds/move.mp3')
        )
        self.capture_sound = Sound(
            os.path.join('sounds/capture.mp3')
        )
        self.promote_sound = Sound(
            os.path.join('sounds/promote.mp3')
        )
        self.check_sound = Sound(
            os.path.join('sounds/check.mp3')
        )
        self.castle_sound = Sound(
            os.path.join('sounds/castle.mp3')
        )

    def changeTheme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def addThemes(self):
        green = Theme((233,237,204),(119,153,84),"#F4F680","#BBCC44","#C8CCAF","#668348")
        brown = Theme((235,209,166),(165,117,80),(245,234,100),(209,185,59),"#C8CCAF","#668348")
        blue = Theme((229,228,200),(60,95,135),(123,187,227),(43,119,191),"#C8CCAF","#668348")
        gray = Theme((120,119,118),(86,85,84),(99,126,143),(82,102,128),"#C8CCAF","#668348")

        self.themes = [green,brown, blue, gray]
