import json

class GameStats:
    """Track the statistics for alien invasion"""

    def __init__(self,ai_game):
        """Initialize the stats"""
        self.settings = ai_game.settings
        #start the game in paused state
        self.game_active = False
        #setting the highest score
        self.high_score = self.load_high_score()
        self.level = 1
        self.reset_stats()

    def reset_stats(self):
        """Initialize the stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    
    def save_high_score(self):
        json_data = {
            'high_score': self.high_score
        }
        with open('score.json','w') as fo:
            json.dump(json_data,fo)
    
    def load_high_score(self):
        try:
            with open('score.json','r') as fo:
                json_data = json.load(fo)
            return json_data['high_score']
        except FileNotFoundError:
            return 0