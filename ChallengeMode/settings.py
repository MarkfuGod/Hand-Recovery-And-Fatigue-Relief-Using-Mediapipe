import pygame

WINDOW_NAME = "HandGesture Master"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700

FPS = 90
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (240, 90)
HAND_SIZE = 200
HAND_HITBOX_SIZE = (60, 80)
HANDGESTURES_SIZES = (50, 38)
HANDGESTURE_SIZE_RANDOMIZE = (1,2) # for each new hand gesture, it will multiply the size with an random value beteewn X and Y
BOMB_SIZES = (50, 50)
BOMB_SIZE_RANDOMIZE = (1.2, 1.5)

# drawing
DRAW_HITBOX = False # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.08 # the frame of the hand gestures will change every X sec

# difficulty
GAME_DURATION = 60 # the game will last X sec
HANDGESTURES_SPAWN_TIME = 1
HANDGESTURES_MOVE_SPEED = {"min": 1, "max": 5}
BOMB_PENALITY = 1 # will remove X of the score of the player (if he kills a bomb)

# colors
COLORS = {"title": (38, 61, 39), "score": (38, 61, 39), "timer": (38, 61, 39),
            "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255),
                        "text": (255, 255, 255), "shadow": (46, 54, 163)}} # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0.16 # value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font("Silver.ttf", 40)
FONTS["medium"] = pygame.font.Font("Silver.ttf", 72)
FONTS["big"] = pygame.font.Font("Silver.ttf", 120)
