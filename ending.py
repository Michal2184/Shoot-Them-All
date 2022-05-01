import pygame


class GameOver:

    def __init__(self, ai_game):
        self.screen = ai_game.screen  # assing screen to attribute ship
        self.screen_rect = ai_game.screen.get_rect()  # helps to put ship at right location

        """ load the ship image """
        self.image = pygame.image.load('images/Game_Over.jpg')

        # get the rectangular area of the Surface
        self.rect = self.image.get_rect()

        """ start each new ship at the bottom of the screen-declate position """
        self.rect.midtop = self.screen_rect.midtop


    def blitme(self):
        """ load ship to the screen  """
        self.screen.blit(self.image, self.rect)
