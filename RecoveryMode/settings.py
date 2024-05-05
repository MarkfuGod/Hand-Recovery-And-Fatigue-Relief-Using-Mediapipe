import pygame

WINDOW_NAME = "HandGesture Master"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700

FPS = 60
DRAW_FPS = False

# sizes
# for each new hand gesture, it will multiply the size with a random value beteewn X and Y
SCROLL_BAR_SIZES = (1000, 133)
CARD_SIZES = (100, 120)
TIP_BOX_SIZE = (100, 100)
exhibit_pos = (200, 180)
TIP_BOX_POS = (200, 280)
rect_size = (200, 500, 100, 100)

# button
BUTTONS_SIZES = (100, 100)
BUTTON_PAUSE_POSITION = (20, 170)
BUTTON_RETURN_POSITION = (20, 295)
BUTTON_NEXT_POSITION = (20, 420)
BUTTON_MUTE_POSITION = (20, 545)

# drawing
DRAW_HITBOX = False  # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.08  # the frame of the hand gestures will change every X sec

# difficulty
GAME_DURATION = 60  # the game will last X sec
HANDGESTURES_SPAWN_TIME = 1
HANDGESTURES_MOVE_SPEED = {"min": 1, "max": 5}
BOMB_PENALITY = 1  # will remove X of the score of the player (if he kills a bomb)

# colors
COLORS = {"title": (38, 61, 39), "score": (38, 61, 39), "timer": (38, 61, 39),
          "buttons": {"default": (56, 67, 209), "second": (87, 99, 255),
                      "text": (255, 255, 255),
                      "shadow": (46, 54, 163)}}  # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0.16  # value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {"small": pygame.font.Font("Silver.ttf", 18), "medium": pygame.font.Font("Silver.ttf", 72),
         "big": pygame.font.Font("Silver.ttf", 120)}
LANE_COORDINATE = [(1250, 180), (1250, 335), (1250, 490)]

# screen
background = pygame.image.load("Assets/background.png")
# 缩放背景图片以匹配窗口大小
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background.get_rect(topleft=(0, 0))
video_background = pygame.image.load("Assets/bar/back.png")
video_background = pygame.transform.scale(video_background, (800, 500))
video_back_rect = video_background.get_rect(topleft=(250,150))
# screen
bar = pygame.image.load("Assets/bar/scroll.png")
bar = pygame.transform.scale(bar,(1050,150))
bar_rect = bar.get_rect(topleft=(80, 0))