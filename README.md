# Platformer_game_maker_pygame

Make a new file, and import the Game file.

Init the constants vars

```
# Initialise window
init_obj = Game.Game.init()

init_obj.Window((0,0), FULLSCREEN=True)

# Get display resolution

display_resolution = init_obj.WIN_X, init_obj.WIN_Y

# init other vars
init_obj.Player((100, 117),NO_JUMPS=4,player_img_path__facing_left=r"C:\Users\wong2\PycharmProjects\GameMaker\imgs\player.png")
init_obj.SetActionKeys((pygame.K_w, pygame.K_UP), ((pygame.K_a, pygame.K_d), (pygame.K_LEFT, pygame.K_RIGHT)),
                       ((pygame.K_e, pygame.K_r), (pygame.K_RCTRL, pygame.K_RSHIFT)))

init_obj.Bullet(25,  r"C:\Users\wong2\PycharmProjects\GameMaker\imgs\bullet.png",4)

init_obj.Terrain(r"C:\Users\wong2\PycharmProjects\GameMaker\imgs\Terrain.png", (sizeX,sizeY))

display_resolution = init_obj.WIN_X, init_obj.WIN_Y
obstacles_post = []
```
There are other params for the init of the players, view the code to view the params


The obstacle post list will be coordinates to be passed on to the Game loop command, which will place the obstacles on screen

` Game.run_game(init_obj,obstacles_post, fill_base=True) `
