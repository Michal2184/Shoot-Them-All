import pygame.font


class InfoMessage:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        """ dims and properties  """
        self.width, self.height = 900, 50
        self.button_color = (204, 6, 6)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('images/Retro_Gaming.ttf', 24)

        """ get  rect object and center it """
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 150

        """ push the message """
        self._prep_msg()

    def _prep_msg(self):
        """ render text into image """
        message = 'STEER - with arrows, SPACE - fire missile, ESC - quit'
        self.info_msg_image = self.font.render(message, True, self.text_color,
                                               self.button_color)
        self.info_msg_image_rect = self.info_msg_image.get_rect()
        self.info_msg_image_rect.center = self.rect.center

    def draw_info(self):
        """ draw square and then draw message on top """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.info_msg_image, self.info_msg_image_rect)


class Title:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 900, 100
        self.button_color = (204, 6, 6)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('images/Retro_Gaming.ttf', 46)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = self.screen_rect.midtop
        self.rect.y += 150

        self.prep_title()

    def prep_title(self):
        """ render text into image """
        message = 'Shoot Them All - by Michal'
        self.info_msg_image = self.font.render(message, True, self.text_color,
                                               self.button_color)
        self.info_msg_image_rect = self.info_msg_image.get_rect()
        self.info_msg_image_rect.center = self.rect.center


    def draw_title(self):
        """ draw square and then draw message on top """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.info_msg_image, self.info_msg_image_rect)
