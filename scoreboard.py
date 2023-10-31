import pygame.font

from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class report scoring information"""

    def __init__(self,ai_game):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        #preparing initial score image
        self.prep_score()

        #preparing initial high score
        self.prep_high_score()

        #preparing the level
        self.prep_level()

        #preparing the ships
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        round_score = round(self.stats.score,-1)
        score_str = "Score: " + "{:,}".format(round_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)

        #display the score at the top right of the screen

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Render the image of the high score"""
        round_high_score = round(self.stats.high_score,-1)
        high_score_str = "High Score: " + "{:,}".format(round_high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)

        # display the high score on left top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Render the image of the current level"""
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)

        #display the level in the center
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """Renders the images of the remaining lives"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship_image = ship.image
            scaled_image = pygame.transform.scale(ship_image,(ship_image.get_width() // 2,ship_image.get_height() // 2))
            ship.image = scaled_image
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 5
            
            self.ships.add(ship)
        

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check if there is a new high score"""
        if self.stats.score>self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()