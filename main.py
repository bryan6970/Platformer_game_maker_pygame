import Game
import pygame

# Initialise stuff
init_obj = Game.Game.init()

init_obj.Window((0, 0), FULLSCREEN=True)
init_obj.Player((100, 117), NO_JUMPS=4,
                player_img_path__facing_left=r"imgs/player.png",
                injured_player_sound_path="sound effects/injured.mp3", PLAYER_SPEED=7)
init_obj.SetActionKeys((pygame.K_w, pygame.K_UP), ((pygame.K_a, pygame.K_d), (pygame.K_LEFT, pygame.K_RIGHT)),
                       ((pygame.K_e, pygame.K_r), (pygame.K_RCTRL, pygame.K_RSHIFT)))

init_obj.Bullet(25, r"imgs\bullet.png", 4,
                gun_start_reload_sound_path=r"sound effects/Start_reload.mp3",
                gun_end_reload_sound_path=r"sound effects/Finish reload.mp3",
                gun_fire_sound_path="sound effects/Gun fire.mp3",
                RELOAD_TIME_SECONDS=3)

init_obj.Terrain(r"imgs\Terrain.png")

display_resolution = init_obj.WIN_X, init_obj.WIN_Y

# put it in an tuple with xy cords. defualt terrain size is 87.75
obstacles_post = [(1, 4)]

obstacles_post = [(x * 87.5, 1080 - y * 87.5) for x, y in obstacles_post]


Game.run_game(init_obj, obstacles_post, fill_base=True)
