import Game
import pygame

# Initialise stuff
init_obj = Game.Game.init()

init_obj.Window((0, 0), FULLSCREEN=True)

display_resolution = init_obj.WIN_X, init_obj.WIN_Y

init_obj.Player((100, 117), NO_JUMPS=4,
                player_img_path__facing_left=r"C:\Users\wong2\PycharmProjects\GameMaker\imgs\player.png")
init_obj.SetActionKeys((pygame.K_w, pygame.K_UP), ((pygame.K_a, pygame.K_d), (pygame.K_LEFT, pygame.K_RIGHT)),
                       ((pygame.K_e, pygame.K_r), (pygame.K_RCTRL, pygame.K_RSHIFT)))

init_obj.Bullet(25, r"C:\Users\wong2\PycharmProjects\GameMaker\imgs\bullet.png", 4,
                gun_fire_sound_path=r"C:\Users\wong2\PycharmProjects\GameMaker\mixkit-game-gun-shot-1662.mp3",
                RELOAD_TIME_SECONDS=10)

init_obj.Terrain(r"C:\Users\wong2\PycharmProjects\GameMaker\imgs\Terrain.png",(display_resolution[0] / 10,display_resolution[0] / 10 ))

# init_obj.Terrain(terrain_size=(display_resolution[0] / 10))

obstacles_post = []

Game.run_game(init_obj, obstacles_post, fill_base=True)
