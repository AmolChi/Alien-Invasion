class Settings:
    """A class to store all settings for alien invasion"""

    def __init__(self):
        """Initialize game settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        
        #bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (30,30,30)
        #this will make the user more accurate
        self.allowed_bullets = 10

        #this is the drop speed of the aliens
        self.fleet_drop_speed = 10

        #for statistics
        self.ship_limit = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        #score increase
        self.score_scale = 1.5

        #score for killing an alien
        self.alien_points = 50

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""

        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 2.0

        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)