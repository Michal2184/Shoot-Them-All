import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        """ load image for alien """
        self.image = pygame.image.load('images/alien2.png')
        self.rect = self.image.get_rect()

        """ declare and space position of alien 1 from side and 1 from top """
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        """ store alien horizontal position """
        self.x = float(self.rect.x)

    def update(self):
        """ move alien to the right """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True

    def hit_sound(self):
        hit = pygame.mixer.Sound('sounds/alien_hit.wav')
        hit.play()