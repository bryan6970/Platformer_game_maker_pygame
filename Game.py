import os

import pygame
import sys
import math
import logging as log
import time


log.basicConfig(filename='game_creater.log', format='%(asctime)s:%(name)s:%(message)s')


class Game:
    def __init__(self,init_object, obstacles_x_y_pos=None, fill_base=True):
        self.constants = init_object

        self.display_resolution = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.Player1 = Player(init_object,0, self.constants.player1_position, self.display_resolution)
        self.Player2 = Player(init_object, 1, self.constants.player2_position, self.display_resolution)
        self.Player1_GUN = Gun(init_object, 0, self.constants.player1_position, self.Player1, self.Player2)
        self.Player2_GUN = Gun(init_object, 1, self.constants.player2_position, self.Player1, self.Player2)

        self.base = []
        self.objects = []

        if fill_base:
            for x in range(math.ceil(self.constants.win.get_width() / self.constants.TERRAIN_SIZE)):
                base = Object(self.constants,
                              (x * self.constants.TERRAIN_SIZE, self.constants.win.get_height() - self.constants.TERRAIN_SIZE))
                self.objects.append(base)

        for x in range(len(obstacles_x_y_pos)):
            self.objects.append(Object(init_object, obstacles_x_y_pos[x]))


    class init:
        win = None

        def __init__(self):
            pygame.init()

            self.win = None
            self.WIN_X = None
            self.WIN_Y = None
            self.PLAYER_X = None
            self.PLAYER_Y = None
            self.TERRAIN_SIZE = None
            self.BULLET_SIZE = None
            self.BULLET_DISTANCE_RATIO = None
            self.BULLET_DISTANCE_FROM_PLAYER = None
            self.PLAYER1_IMG = None
            self.PLAYER2_IMG = None
            self.TERRAIN_IMG = None
            self.PLAYER1_BULLET = None
            self.PLAYER2_BULLET = None
            self.PLAYER_SPEED = None
            self.BULLET_SPEED = None
            self.MAGAZINE_SIZE = None
            self.RELOAD_TIME_SECONDS = None
            self.PLAYER_HEALTH = None
            self.GRAVITY = None
            self.PLAYER_JUMP_FORCE = None
            self.NO_JUMPS = None
            self.TERRAIN_PLAYER_BORDER_X = 0
            self.TERRAIN_PLAYER_BORDER_Y = 0
            self.player1_position = None
            self.player2_position = None

            self.PLAYER1_MOVEMENT_KEYS = None
            self.PLAYER2_MOVEMENT_KEYS = None

            self.PLAYER1_FIRE_KEY = None
            self.PLAYER1_RELOAD_KEY = None
            self.PLAYER2_FIRE_KEY = None
            self.PLAYER2_RELOAD_KEY = None
            self.PLAYER1_JUMP_KEY = None
            self.PLAYER2_JUMP_KEY = None

        def Window(self,win_size: tuple,  FULLSCREEN=False):
            if FULLSCREEN:
                self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                win = self.win
            else:
                self.win = pygame.display.set_mode(win_size)
                win = self.win

            self.WIN_X = pygame.display.get_window_size()[0]
            self.WIN_Y = pygame.display.get_window_size()[1]

        def Player(self, player_size: tuple, player_img_path__facing_left: str, PLAYER_SPEED=5,
         left_player_starting_pos: tuple = "default",PLAYER_HEALTH=5, GRAVITY=0.05, PLAYER_JUMP_FORCE=7.5, NO_JUMPS=2):

            # Set constants
            self.PLAYER_SPEED = PLAYER_SPEED
            self.PLAYER_HEALTH = PLAYER_HEALTH
            self.GRAVITY = GRAVITY
            self.PLAYER_JUMP_FORCE = PLAYER_JUMP_FORCE
            self.NO_JUMPS = NO_JUMPS

            self.PLAYER_X, self.PLAYER_Y = player_size

            # Scale imgs
            self.PLAYER1_IMG = pygame.transform.scale(pygame.image.load(player_img_path__facing_left).convert_alpha(),player_size)

            self.PLAYER2_IMG = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(player_img_path__facing_left)).convert_alpha(),player_size), True, False)

            # Get player starting pos
            if left_player_starting_pos == "default":
                self.player1_position = (self.WIN_X - self.PLAYER_X) / 4, (self.WIN_Y - self.PLAYER_Y) / 2
                self.player2_position = (self.WIN_X - self.PLAYER_X) / 4 * 3, (self.WIN_Y - self.PLAYER_Y) / 2

            else:
                self.player1_position = left_player_starting_pos
                self.player2_position = self.WIN_X - left_player_starting_pos[0] - self.PLAYER_X, self.WIN_Y - left_player_starting_pos[
                    1] - self.PLAYER_Y

        def SetActionKeys(self,jump_keys: tuple, movement_keys__both_players: tuple, fire_reload_keys__both_players: tuple):
            """
            :param jump_keys: use pygame.(key). Order is P1, P2
            :param movement_keys__both_players: LEFT_RIGHT, use pygame.(key). Order is P1, P2
            :param fire_reload_keys__both_players: FIRE, RELOAD, use pygame.(key). Order is P1, P2
            :return: None
            """

            if len(movement_keys__both_players) == 4:
                self.PLAYER1_MOVEMENT_KEYS = movement_keys__both_players[0], movement_keys__both_players[1]
                self.PLAYER2_MOVEMENT_KEYS = movement_keys__both_players[2], movement_keys__both_players[3]

            elif len(movement_keys__both_players) == 2:
                self.PLAYER1_MOVEMENT_KEYS = movement_keys__both_players[0]
                self.PLAYER2_MOVEMENT_KEYS = movement_keys__both_players[1]

            else:
                raise ValueError("Make sure each player has 4 keys tied to them")

            self.PLAYER1_JUMP_KEY = jump_keys[0]
            self.PLAYER2_JUMP_KEY = jump_keys[1]

            if len(fire_reload_keys__both_players) == 2:
                self.PLAYER1_FIRE_KEY = fire_reload_keys__both_players[0][0]
                self.PLAYER1_RELOAD_KEY = fire_reload_keys__both_players[0][1]

                self.PLAYER2_FIRE_KEY = fire_reload_keys__both_players[1][0]
                self.PLAYER2_RELOAD_KEY = fire_reload_keys__both_players[0][1]

            elif len(fire_reload_keys__both_players) == 4:
                self.PLAYER1_FIRE_KEY = fire_reload_keys__both_players[0]
                self.PLAYER1_RELOAD_KEY = fire_reload_keys__both_players[1]
                self.PLAYER2_FIRE_KEY = fire_reload_keys__both_players[2]
                self.PLAYER2_RELOAD_KEY = fire_reload_keys__both_players[3]

            else:
                raise ValueError("Make sure each player has 4 keys tied to them")

            log.info('Keys init, Game started')
            log.debug(
                f"Keys values = {self.PLAYER1_MOVEMENT_KEYS, self.PLAYER2_MOVEMENT_KEYS, self.PLAYER1_FIRE_KEY, self.PLAYER1_RELOAD_KEY, self.PLAYER2_FIRE_KEY, self.PLAYER2_RELOAD_KEY, self.PLAYER1_JUMP_KEY, self.PLAYER2_JUMP_KEY}")

        def Bullet(self ,bullet_size: int, bullet_img_path__facing_left: str, top_of_player_to_bullet__dist_ratio: int,  BULLET_SPEED=15, MAGAZINE_SIZE=10, RELOAD_TIME_SECONDS=5,):

            self.BULLET_SIZE = bullet_size
            self.BULLET_SPEED = BULLET_SPEED
            self.BULLET_DISTANCE_RATIO = top_of_player_to_bullet__dist_ratio
            self.BULLET_DISTANCE_FROM_PLAYER = self.PLAYER_Y / self.BULLET_DISTANCE_RATIO

            self.MAGAZINE_SIZE = MAGAZINE_SIZE
            self.RELOAD_TIME_SECONDS = RELOAD_TIME_SECONDS

            self.PLAYER1_BULLET = pygame.transform.scale(
                pygame.image.load(bullet_img_path__facing_left),
                (bullet_size, bullet_size))
            self.PLAYER2_BULLET = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load(os.path.join(bullet_img_path__facing_left)),
                                       (bullet_size, bullet_size)), True,
                False)

        def Terrain(self, terrain_img_path: str, terrain_size: int = 'default'):

            if terrain_size == 'default':
                self.TERRAIN_SIZE = self.PLAYER_Y / 4 * 3
            else:
                self.TERRAIN_SIZE = terrain_size

            self.TERRAIN_IMG = pygame.transform.scale((pygame.image.load(terrain_img_path)), (self.TERRAIN_SIZE, self.TERRAIN_SIZE))

    def _check_collide_player(self, player_number: int, left_opponent_bullet_list: list,
                              right_opponent_bullet_list: list):
        """
        :param player_number: (int) 0 for player 1, 1 for player 2
        :param right_opponent_bullet_list: list of opponent (x, y ) bullet positions
        :param left_opponent_bullet_list: list of opponent (x, y) bullet positions
        :return: Number of bullets that hit
        """

        score = 0
        if player_number == 0:
            for i, bullet in enumerate(left_opponent_bullet_list):

                if self.Player1.rect.colliderect(bullet):
                    score += 1
                    left_opponent_bullet_list.remove(bullet)

                if (bullet[0] < -self.constants.BULLET_SIZE) or bullet[0] > self.display_resolution[0]:
                    left_opponent_bullet_list.remove(bullet)

            for i, bullet in enumerate(right_opponent_bullet_list):

                if self.Player1.rect.colliderect(bullet):
                    score += 1
                    right_opponent_bullet_list.remove(bullet)

                if (bullet[0] < -self.constants.BULLET_SIZE) or bullet[0] > self.display_resolution[0]:
                    right_opponent_bullet_list.remove(bullet)

        elif player_number == 1:
            for i, bullet in enumerate(left_opponent_bullet_list):
                if self.Player2.rect.colliderect(bullet):
                    score += 1
                    left_opponent_bullet_list.remove(bullet)

                if (bullet[0] < -self.constants.BULLET_SIZE) or bullet[0] > self.display_resolution[0]:
                    left_opponent_bullet_list.remove(bullet)

            for i, bullet in enumerate(right_opponent_bullet_list):
                if self.Player2.rect.colliderect(bullet):
                    score += 1
                    right_opponent_bullet_list.remove(bullet)

                if (bullet[0] < -self.constants.BULLET_SIZE) or bullet[0] > self.display_resolution[0]:
                    right_opponent_bullet_list.remove(bullet)

        # print('score:', score)
        return score, left_opponent_bullet_list, right_opponent_bullet_list

    def run_game(self, movement_input_list, gun_input_list, running_fps: float):
        """
        :param running_fps: FPS that the machine is running the game at
        :param gun_input_list: bool values ((a,b)(block,y)) a, b for p1 inputs and block, y for p2 inputs following FIRE WEAPON and RELOAD WEAPON
        :param movement_input_list: bool values ((a,b)(block,y)) a, b for p1 inputs and block, y for p2 inputs following UP DOWN LEFT RIGHT order
        :returns: None
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        PLAYER1_FIRE = gun_input_list[0][0]
        PLAYER2_FIRE = gun_input_list[1][0]

        PLAYER1_RELOAD = gun_input_list[0][1]
        PLAYER2_RELOAD = gun_input_list[1][1]

        self.constants.win.fill((0, 0, 0))

        # print(movement_input_list)
        self.Player1.move(movement_input_list[0], running_fps)
        self.Player2.move(movement_input_list[1], running_fps)

        for block in self.base:
            block.check_collision_player(self.Player1)
            block.check_collision_player(self.Player2)

            self.Player1_GUN.LEFT_BULLET_RECTS, self.Player1_GUN.RIGHT_BULLET_RECTS = block.check_collision_bullet(
                self.Player1_GUN.LEFT_BULLET_RECTS, self.Player1_GUN.RIGHT_BULLET_RECTS)
            self.Player2_GUN.LEFT_BULLET_RECTS, self.Player2_GUN.RIGHT_BULLET_RECTS = block.check_collision_bullet(
                self.Player2_GUN.LEFT_BULLET_RECTS, self.Player2_GUN.RIGHT_BULLET_RECTS)

            self.constants.win.blit(block.image, (block.x_pos, block.y_pos))

        for object_ in self.objects:
            object_.check_collision_player(self.Player1)
            object_.check_collision_player(self.Player2)

            self.Player1_GUN.LEFT_BULLET_RECTS, self.Player1_GUN.RIGHT_BULLET_RECTS = object_.check_collision_bullet(
                self.Player1_GUN.LEFT_BULLET_RECTS, self.Player1_GUN.RIGHT_BULLET_RECTS)
            self.Player2_GUN.LEFT_BULLET_RECTS, self.Player2_GUN.RIGHT_BULLET_RECTS = object_.check_collision_bullet(
                self.Player2_GUN.LEFT_BULLET_RECTS, self.Player2_GUN.RIGHT_BULLET_RECTS)

            self.constants.win.blit(object_.image, (object_.x_pos, object_.y_pos))

        self.Player1_GUN.run_gun((self.Player1.rect.x, self.Player1.rect.y), PLAYER1_FIRE, PLAYER1_RELOAD)
        self.Player2_GUN.run_gun((self.Player2.rect.x, self.Player2.rect.y), PLAYER2_FIRE, PLAYER2_RELOAD)

        PLAYER1_HIT_ENEMY, self.Player1_GUN.LEFT_BULLET_RECTS, self.Player1_GUN.RIGHT_BULLET_RECTS = \
            self._check_collide_player(
                1, self.Player1_GUN.LEFT_BULLET_RECTS, self.Player1_GUN.RIGHT_BULLET_RECTS)
        PLAYER2_HIT_ENEMY, self.Player2_GUN.LEFT_BULLET_RECTS, self.Player2_GUN.RIGHT_BULLET_RECTS = \
            self._check_collide_player(
                0, self.Player2_GUN.LEFT_BULLET_RECTS, self.Player2_GUN.RIGHT_BULLET_RECTS)

        self.Player1.score += PLAYER1_HIT_ENEMY
        self.Player2.score += PLAYER2_HIT_ENEMY

        self.Player1.health -= PLAYER2_HIT_ENEMY
        self.Player2.health -= PLAYER1_HIT_ENEMY

        self.constants.win.blit(self.Player1.IMG, self.Player1.rect)
        self.constants.win.blit(self.Player2.IMG, self.Player2.rect)

        for bullet_position in self.Player1_GUN.LEFT_BULLET_RECTS:
            self.constants.win.blit(self.Player2_GUN.BULLET_IMG, bullet_position)

        for bullet_position in self.Player1_GUN.RIGHT_BULLET_RECTS:
            self.constants.win.blit(self.Player1_GUN.BULLET_IMG, bullet_position)

        for bullet_position in self.Player2_GUN.LEFT_BULLET_RECTS:
            self.constants.win.blit(self.Player2_GUN.BULLET_IMG, bullet_position)

        for bullet_position in self.Player2_GUN.RIGHT_BULLET_RECTS:
            self.constants.win.blit(self.Player1_GUN.BULLET_IMG, bullet_position)

        # print(self.Player1.health,self.Player2.health)

        if self.Player1.health <= 0 or self.Player2.health <= 0:
            sys.exit()

        pygame.display.update()

class Player:
    def __init__(self,init_obj, player_number: int, player_position: list, display_resolution_width_height: tuple):
        self.init_obj = init_obj

        self.player_number = player_number
        self.health = init_obj.PLAYER_HEALTH
        self.score = 0
        self.IMG = init_obj.PLAYER1_IMG if player_number == 0 else init_obj.PLAYER2_IMG
        self.mask = pygame.mask.from_surface(self.IMG)
        self.rect = self.mask.get_rect(topleft=[player_position[1], player_position[1]])

        # self.rect.inflate_ip(-self.rect.width,-self.rect.height)
        self.IMG = self.IMG.convert_alpha()
        self.rect = self.IMG.get_bounding_rect()
        self.rect.x = player_position[0]
        self.rect.y = player_position[1]

        self.flipped = False

        self.display_resolution = display_resolution_width_height
        self.tick_count = 0

        self.y_velocity = 0
        self.x_velocity = 0

        self.width = self.rect.width
        self.height = self.rect.height

        self.jumps = 0

    def _jump(self):
        if self.jumps > 0:
            self.y_velocity = min(-self.init_obj.PLAYER_JUMP_FORCE, self.y_velocity - self.init_obj.PLAYER_JUMP_FORCE)

            if self.y_velocity < -self.init_obj.PLAYER_JUMP_FORCE:
                self.y_velocity = -self.init_obj.PLAYER_JUMP_FORCE

            self.tick_count = 1
            self.jumps -= 1
            log.debug(f'Player {self.player_number} jumped')

    def move(self, input_list_JUMP_LEFT_RIGHT: list, ticks_per_second: float):
        if ticks_per_second == 0:
            ticks_per_second = 1

        if input_list_JUMP_LEFT_RIGHT[0]:
            self._jump()

        if input_list_JUMP_LEFT_RIGHT[1]:
            self.x_velocity = -self.init_obj.PLAYER_SPEED
        elif input_list_JUMP_LEFT_RIGHT[2]:
            self.x_velocity = +self.init_obj.PLAYER_SPEED
        else:
            self.x_velocity = 0

        self.rect.x += self.x_velocity

        self.tick_count += 1

        self.y_velocity = self.y_velocity + (
                self.init_obj.GRAVITY * (self.tick_count / ticks_per_second * 30))  # physics equation

        self.rect.y += self.y_velocity

        log.info(f'player {self.player_number} speed (x, y) {self.x_velocity, self.y_velocity}')

        self._check_off_screen()

        log.info(f'player {self.player_number} position (x, y) {self.rect.x, self.rect.y}')

        if self.player_number == 0:
            if self.x_velocity < 0 and not self.flipped:
                self._flip_img(True)
            elif self.x_velocity > 0 and self.flipped:
                self._flip_img(False)
        elif self.player_number == 1:
            if self.x_velocity > 0 and not self.flipped:
                self._flip_img(True)
            elif self.x_velocity < 0 and self.flipped:
                self._flip_img(False)

    def _check_off_screen(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > (self.display_resolution[0] - self.init_obj.PLAYER_X):
            self.rect.x = self.display_resolution[0] - self.init_obj.PLAYER_X

        if self.rect.y < 0:
            self.rect.y = 0
            self.y_velocity = 0
        elif self.rect.y > (self.display_resolution[1] - self.init_obj.PLAYER_Y):
            self.rect.y = self.display_resolution[1] - self.init_obj.PLAYER_Y
            self.y_velocity = 0
            self.jumps = self.init_obj.NO_JUMPS

    def _flip_img(self, flip_img):
        self.IMG = pygame.transform.flip(self.IMG, True, False)
        self.flipped = flip_img


class Object:
    def __init__(self,init_obj,position: tuple):

        self.constants = init_obj


        self.image = init_obj.TERRAIN_IMG
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=[position[0], position[1]])

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.object_center_x = self.x_pos + self.width / 2
        self.object_center_y = self.y_pos + self.height / 2

    def check_collision_player(self, player: object):

        if not self.rect.colliderect(player.rect):
            pass
        else:
            # Create a dictionary to store the collision sides
            collision_sides = {'left': False, 'right': False, 'top': False, 'bottom': False}

            # Check for collision
            if self.rect.colliderect(player.rect):

                # Find dist of all sides

                top = abs(self.rect.top - player.rect.bottom)
                bottom = abs(self.rect.bottom - player.rect.top)
                left = abs(self.rect.left - player.rect.right)
                right = abs(self.rect.right - player.rect.left)

                directions = [top, bottom, left, right]
                # print(directions)

                index = directions.index(min(top, bottom, left, right))

                if index == 0:
                    player.y_velocity = 0

                    player.rect.bottom = self.rect.top
                    player.jumps = self.constants.NO_JUMPS
                    player.tick_count = 1

                elif index == 1:
                    player.y_velocity *= -1

                    player.rect.top = self.rect.bottom

                elif index == 2:
                    player.x_velocity *= -1

                    player.rect.right = self.rect.left

                elif index == 3:
                    player.x_velocity *= -1

                    player.rect.left = self.rect.right



    def check_collision_bullet(self, left_bullet_rects: list, right_bullet_rects: list):
        """
        "Only works in pygame"
        :param left_bullet_rects: rectangles of the bullets
        :param right_bullet_rects: rectangles of the bullets
        :return: bullet rects
        """

        i = self.rect.collidelist(right_bullet_rects)
        x = self.rect.collidelist(left_bullet_rects)

        if x >= 0:
            del left_bullet_rects[i]
            log.debug('Player got hit')
        if i >= 0:
            del right_bullet_rects[i]
            log.debug('Player got hit')

        return left_bullet_rects, right_bullet_rects



class Gun:
    def __init__(self,init_obj, player_number, player_position, player1, player2):
        self.init_obj = init_obj

        self.BULLET_IMG = self.init_obj.PLAYER1_BULLET if player_number == 0 else self.init_obj.PLAYER2_BULLET
        self.BULLET_IMG_MASK = pygame.mask.from_surface(self.BULLET_IMG)
        self.LEFT_BULLET_RECTS = []
        self.RIGHT_BULLET_RECTS = []

        self.player_number = player_number

        self.x = player_position[0]
        self.y = player_position[1]

        self.Magazine_size = self.init_obj.MAGAZINE_SIZE
        self.magazine = self.Magazine_size
        self.bullet_speed = self.init_obj.BULLET_SPEED

        self.bullets = []
        self.left_direction_bullets = []
        self.right_direction_bullets = []
        self.reloading = False

        self.Player1 = player1
        self.Player2 = player2

    def run_gun(self, player_position, Fire_weapon=False, Reload_weapon=False):
        self.x = player_position[0]
        self.y = player_position[1]

        # print(self.magazine)
        if Reload_weapon or self.magazine == 0:
            # print('reloading')
            self._reload()

        if self.magazine > 0 and not self.reloading:
            if Fire_weapon:
                self.magazine -= 1
                # print(self.magazine)
                self._shoot()

        self._move_bullets()

    def _shoot(self):
        if self.player_number == 0:
            if self.Player1.flipped:
                self.left_direction_bullets.append(
                    self.BULLET_IMG.get_rect(topleft=[self.x, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER]))

                self.LEFT_BULLET_RECTS.append(
                    self.BULLET_IMG.get_rect(topleft=[self.x, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER]))
            else:
                self.right_direction_bullets.append(self.BULLET_IMG.get_rect(
                    topleft=[self.x + self.init_obj.PLAYER_X, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER]))

                self.RIGHT_BULLET_RECTS.append(self.BULLET_IMG.get_rect(
                    topleft=[self.x + self.init_obj.PLAYER_X, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER]))

        else:
            if self.Player2.flipped:
                self.right_direction_bullets.append(self.BULLET_IMG.get_rect(
                    topleft=[self.x + self.init_obj.PLAYER_X, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER])
                )
                self.RIGHT_BULLET_RECTS.append(
                    self.BULLET_IMG.get_rect(
                        topleft=[self.x + self.init_obj.PLAYER_X, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER]))

            else:
                self.left_direction_bullets.append(
                    self.BULLET_IMG.get_rect(topleft=[self.x, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER]))
                self.LEFT_BULLET_RECTS.append(
                    self.BULLET_IMG.get_rect(topleft=[self.x, self.y + self.init_obj.BULLET_DISTANCE_FROM_PLAYER]))

        # print(self.bullets)

    def _move_bullets(self):
        for i, bullet in enumerate(self.left_direction_bullets):
            self.left_direction_bullets[i][0] -= self.init_obj.BULLET_SPEED

        for i, bullet in enumerate(self.right_direction_bullets):
            self.right_direction_bullets[i][0] += self.init_obj.BULLET_SPEED

        self.LEFT_BULLET_RECTS = self.left_direction_bullets
        self.RIGHT_BULLET_RECTS = self.right_direction_bullets

        self.bullets.extend(self.left_direction_bullets)
        self.bullets.extend(self.right_direction_bullets)

    def _reload(self):
        if not self.reloading:
            self.current_time = time.time()
            self.reloading = True

        if time.time() - self.current_time > self.init_obj.RELOAD_TIME_SECONDS:
            self.magazine = self.Magazine_size
            self.reloading = False




def run_game(init_obj, obstacles_x_y_pos, fill_base=False):

    game = Game(init_obj, obstacles_x_y_pos, fill_base)
    Clock = pygame.time.Clock()
    while True:
        Clock.tick(60)
        PLAYER1_FIRE = False
        PLAYER2_FIRE = False

        PLAYER1_RELOAD = False
        PLAYER2_RELOAD = False

        PLAYER1_INPUTS = [False, False, False]
        PLAYER2_INPUTS = [False, False, False]

        # print(Clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == init_obj.PLAYER1_FIRE_KEY:
                    PLAYER1_FIRE = True
                    log.info('Player 1 pressed FIRE key')

                if event.key == init_obj.PLAYER1_RELOAD_KEY:
                    PLAYER1_RELOAD = True
                    log.info('Player 1 pressed RELOAD key')

                if event.key == init_obj.PLAYER1_JUMP_KEY:
                    PLAYER1_INPUTS[0] = True
                    log.info('Player 1 pressed JUMP key')

                if event.key == init_obj.PLAYER2_FIRE_KEY:
                    PLAYER2_FIRE = True
                    log.info('Player 2 pressed FIRE key')

                if event.key == init_obj.PLAYER2_RELOAD_KEY:
                    PLAYER2_RELOAD = True
                    log.info('Player 2 pressed RELOAD key')

                if event.key == init_obj.PLAYER2_JUMP_KEY:
                    PLAYER2_INPUTS[0] = True
                    log.info('Player 2 pressed JUMP key')

        for i, key in enumerate(init_obj.PLAYER1_MOVEMENT_KEYS, start=1):
            PLAYER1_INPUTS[i] = pygame.key.get_pressed()[key]

        for i, key in enumerate(init_obj.PLAYER2_MOVEMENT_KEYS, start=1):
            PLAYER2_INPUTS[i] = pygame.key.get_pressed()[key]

        game.run_game((PLAYER1_INPUTS, PLAYER2_INPUTS),

                      ((PLAYER1_FIRE, PLAYER1_RELOAD), (PLAYER2_FIRE, PLAYER2_RELOAD)), Clock.get_fps())
