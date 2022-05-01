import json

class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings

        self.level = 1
        self.reset_stats()
        self.game_active = False
        self.high_score = self.check_record()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def check_record(self):
        filename = 'scores.json'
        with open(filename) as f:
            score = json.load(f)
        return score

