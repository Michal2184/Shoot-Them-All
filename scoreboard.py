import pygame.font
from pygame.sprite import Group
from ship import Ship
import json

class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        """ font settings """
        self.text_color = (39, 69, 242)
        self.font = pygame.font.Font('images/Retro_Gaming.ttf', 24)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "POINTS: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color)  # background?
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        """ make render image of high score """
        high_score = round(self.stats.high_score, -1)
        high_score_str = "HIGH SCORE: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color)
        """ position """
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20


    def check_high_score(self):
        """ check to see if there is new high score """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            filename = 'scores.json'
            with open(filename, 'w') as f:
                json.dump(self.stats.score, f)

    def prep_level(self):
        level = str(self.stats.level)
        level_str = "LV: {:}".format(level)
        self.level_str_image = self.font.render(level_str, True,
                                                self.text_color)
        self.level_rect = self.level_str_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)



    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_str_image, self.level_rect)
        self.ships.draw(self.screen)
