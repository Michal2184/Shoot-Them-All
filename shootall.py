import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from games_stats import GameStats
from button import Button
from front import InfoMessage, Title
from ending import GameOver
from scoreboard import Scoreboard


class ShootThemAll:
    """ class to manage game """

    def __init__(self):
        """ start game and create game resources """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))  # surface of game
        pygame.display.set_caption("*******  SHOOT THEM ALL by Michal *******")
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.alien = Alien(self)
        self.sb = Scoreboard(self)
        self.ending = GameOver(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "CLICK ME")
        self.info_message = InfoMessage(self)
        self.title = Title(self)

    def run_game(self):
        """ start main loop of the game """
        self.settings.game_music_play(True)
        while True:
            self._check_events()

            """ check if False or True and start """
            if self.stats.game_active:
                # self.settings.game_music_play(False)
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            """ print all above to screen 
                ,important very last function outside if statment """
            self._update_screen()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        collide = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        """ check if all aliens destroyed """
        if collide:
            for alien in collide.values():
                self.stats.score += self.settings.alien_points
                self.alien.hit_sound()
                self.sb.prep_score()  # prep to show points on screen , save after
                self.sb.check_high_score()
        if not self.aliens:
            self.bullets.remove()  # remove rself.play_button = Button(self, 'Play Game!')emaining bullets
            self._create_fleet()  # populate screen with new aliens
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()  # wont print new level without it
            self.sb.prep_ships()
            sleep(0.5)

    def _check_events(self):
        """ respond to keypress and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # reads inputs in real time
                sys.exit()  # quits when detect quit call
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # store mouse x,y
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ check if mouse position is above button """
        over_button = self.play_button.rect.collidepoint(mouse_pos)
        if over_button and not self.stats.game_active:
            self.settings.init_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True  # if it is change game state

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)  # hides mouse after start

    def _check_keydown_events(self, event):
        """ continuous movement to the right """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        """ continuous movement to the left """
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        """ quit function """
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        """ fire bullet """
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            new_bullet.play_sound()

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        """ place them with right spacing in """
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height + 2 * alien.rect.height * row_number) + 25

        self.aliens.add(alien)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_hight = self.ship.rect.height
        """ calculate screen size against alien size to find amount needed """
        avalible_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avalible_space_x // (2 * alien_width)
        avalible_space_y = self.settings.screen_height - \
                           (4 * alien_height) - ship_hight
        number_rows = avalible_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            """ print fleet to the screen """
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print(f'\nShip has been destroyed.'
            #     f'\nLives left:{self.stats.ships_left}')
            """ check if ship has been hit """
            self._ship_hit()
        """ looking if aliens hit bottom of the screen """
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.ship.play_hit_sound()
            """ get rid of whats at screen """
            self.bullets.empty()
            self.aliens.empty()

            """ create new fleet """
            self._create_fleet()
            self.ship.center_ship()
            sleep(1.0)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)  # shows mouse

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                # print('Aliens has hit bottom of the screen')
                # print(f'\n Lives left: {self.stats.ships_left}')
                break

    def _update_screen(self):
        # redraw the screen every loop
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.settings.bg_image, self.settings.image_rect)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()  # draw score

        if not self.stats.game_active:
            if self.stats.ships_left == 0:
                self.ending.blitme()  # show game over

            self.play_button.draw_button()
            self.info_message.draw_info()
            self.title.draw_title()

        """ drawing most recent screen , erasing old and printing new """
        pygame.display.flip()  # update the contents of the entire display


if __name__ == '__main__':
    """ activate the game """
    ai = ShootThemAll()
    ai.run_game()
