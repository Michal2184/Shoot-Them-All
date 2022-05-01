import pygame


class Settings:
    """ class sotres all setings for a game """

    def __init__(self):
        """ screen settings """
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_image = pygame.image.load('images/tlo.jpg')
        self.image_rect = self.bg_image.get_rect()
        self.bg_color = (200, 200, 200)  # background

        """ ship settings """
        self.ship_limit = 1

        """ bullet settings """

        self.bullet_width = 4
        self.bullet_height = 18
        self.bullet_color = (255, 40, 0)
        self.bullets_allowed = 5

        """ alien settings """
        self.fleet_drop_speed = 15

        """ game dynamics increase """
        self.speedup_scale = 1.1
        self.init_dynamic_settings()


    def init_dynamic_settings(self):
        self.alien_speed = 0.5
        self.ship_speed = 2.0  # ship speed
        self.bullet_speed = 3.0
        self.fleet_direction = 1  # times one to get positive or -1 for negative
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

    def game_music_play(self, state):
        """ background music """
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/Run.ogg')
        if state:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

