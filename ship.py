import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen  # assing screen to attribute ship
        self.screen_rect = ai_game.screen.get_rect()  # helps to put ship at right location

        """ load the ship image """
        self.image = pygame.image.load('images/ship3.png')

        # get the rectangular area of the Surface
        self.rect = self.image.get_rect()

        """ start each new ship at the bottom of the screen-declate position """
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False

        self.settings = ai_game.settings
        self.x = float(self.rect.x)


    def update(self):

        if self.moving_right and self.rect.right < self.screen_rect.right: #right limit
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > self.screen_rect.left: # left limit
            self.x -= self.settings.ship_speed

        self.rect.x = self.x    #after value change ,new position X value

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

    def play_hit_sound(self):
        ship_destroyed = pygame.mixer.Sound('sounds/ship_hit.wav')
        ship_destroyed.play()

    def blitme(self):
        """ load ship to the screen  """
        self.screen.blit(self.image, self.rect)
