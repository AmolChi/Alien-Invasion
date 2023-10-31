import sys

from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create the resources"""
        #initializes the pygame 
        pygame.init()
        self.settings = Settings()

        #creating stats
        self.stats = GameStats(self)

        #setting the display for the game
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width

        # #sets the screen available for every object of alienInvasion class
        # self.screen = pygame.display.set_mode((1200,800))
        # #initializing the backgroud color
        # self.bg_color = (230,230,230)

        # #sets the display caption as alien invasion
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        #creating button
        self.play_button = Button(self,"Click here to Play Or Press Q to exit")

        #creating score board
        self.sb = Scoreboard(self)

    def run_game(self):
        """Starts the main loop for the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            
    def _update_screen(self):
        """updates the images on the screen and flip to new screen`"""
        #setting the background color
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()
        #displaying the lastest animated screen
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()
        
    def _check_events(self):
        """Responding to click and mouse events"""
        #checking if exit is hit or not
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                 self._check_keyup_events(event)

    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks play""" 
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active: 
            # resetting the dynamic speeds
            self.settings.initialize_dynamic_settings()
            #reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #empty the existing aliens
            self.aliens.empty()
            self.bullets.empty()

            #create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        """Response to keypress events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Repsopnse to key release events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False   
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.allowed_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update the positions of bullets and getting rid of the old bullets"""
        self.bullets.update()
        #getting rid of old bullets which would have taken extra space

        for bullet in self.bullets.copy(): 
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
            self._check_bullet_alien_collision()
    
    def _check_bullet_alien_collision(self):
        #check for any bullets that have hit the aliens, if so then get rid of the bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        #if all aliens are dead create a new fleet
        if not self.aliens:
            #destroy the existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase the level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size

        #determining the number of alien per row
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = (available_space_x // (2*alien_width) ) + 1

        #determining the number of rows
        ship_height = self.ship.rect.height
        available_y = (self.settings.screen_height - (alien_height)- ship_height)
        number_rows = available_y // (2*alien_height)

        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row)

    def _create_alien(self,alien_number,row):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.y = alien.rect.height + 1.25*alien.rect.height*row
        alien.rect.y = alien.y
        self.aliens.add(alien)
    
    def _update_aliens(self):
        """Update the position of all the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #looking for alien ship collision

        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        self._check_aliens_hit_bottom()
    
    def _check_fleet_edges(self):
        """Respond if any alien has met the edges of screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y +=self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1     

    def _ship_hit(self):
        """Respond to hit by ship"""
        if self.stats.ships_left > 0:
            #decrease the number of ships by 1
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of any aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)  
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_hit_bottom(self):
        """Check if any alien hits the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>= screen_rect.bottom:
                #treat if as it hits the ship
                self._ship_hit()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()