import math
import Game
import pygame

import json

with open("config.json", "r") as f:
    data = json.load(f)  # This will parse the JSON into a dictionary


# Initialise stuff
init_obj = Game.Game.init()

init_obj.Window((0, 0), FULLSCREEN=True)


terrain_size = data["TERRAIN_SIZE"]


player_size = data["PLAYER_SIZE"]



bullet_size = data["BULLET_SIZE"]





init_obj.Terrain(r"imgs/Terrain.png",terrain_size=terrain_size)


init_obj.Player(player_size, NO_JUMPS=data["NO_JUMPS"],
                player_img_path_facing_left=r"imgs/player.png",
                injured_player_sound_path="sound effects/injured.mp3", PLAYER_SPEED=data["PLAYER_SPEED"], PLAYER_JUMP_FORCE=data["JUMP_FORCE"],GRAVITY=data["GRAVITY"])
init_obj.SetActionKeys((pygame.K_w, pygame.K_UP), ((pygame.K_a, pygame.K_d), (pygame.K_LEFT, pygame.K_RIGHT)),
                       ((pygame.K_e, pygame.K_r), (pygame.K_RSHIFT, pygame.K_RCTRL)))

init_obj.Bullet(bullet_size, r"imgs/bullet.png", 4,
                gun_start_reload_sound_path=r"sound effects/Start_reload.mp3",
                gun_end_reload_sound_path=r"sound effects/Finish reload.mp3",
                gun_fire_sound_path="sound effects/Gun fire.mp3",
                RELOAD_TIME_SECONDS=data["RELOAD_TIME"], MAGAZINE_SIZE=data["MAGAZINE_SIZE"],BULLET_SPEED=data["BULLET_SPEED"])


display_resolution = init_obj.WIN_X, init_obj.WIN_Y



obstacles_post = data["OBSTACLE_POST"]


if data["MIRROR_TERRAIN"]:

    number_of_tiles_in_a_row = math.ceil(1920 / terrain_size[0])

    obstacles_post.extend([(number_of_tiles_in_a_row - 1 -x,y)for (x,y) in obstacles_post])

obstacles_post = [(x * terrain_size[0],  y * terrain_size[1]) for x, y in obstacles_post]


Game.run_game(init_obj, obstacles_post, fill_base=True)
