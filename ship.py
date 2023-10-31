import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self,ai_game):
        """Initialize the starting position of the ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #load the ship image and get its rect

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Storing the x coordinates of ship
        self.x = float(self.rect.x)
        #movement flags
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on movement of flag"""
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x +=self.settings.ship_speed
        elif self.moving_left and self.rect.left>0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
    
    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        """Center the ship"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)