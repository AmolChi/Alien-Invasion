import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_game):
        """Initialize the alien and set the starting position"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #load the alien image and set its rect attribute

        self.image = pygame.image.load('images/ufo.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return true if alien has hit the edge of the screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left<=0:
            return True

    def update(self):
        """Move the alien"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x