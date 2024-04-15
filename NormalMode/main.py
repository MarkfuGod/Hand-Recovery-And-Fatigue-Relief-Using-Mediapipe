# Setup Python ----------------------------------------------- #
import pygame
import sys
import os

from lane import Lane
from enemy import Enemy, EnemyHandle
from settings import *
from scroll_bar import *
from game import *
from temp_hand_game.NormalMode.ball import BallHandle

# Setup pygame/window --------------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 32)  # windows position
pygame.init()
pygame.display.set_caption(WINDOW_NAME)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Clock ----------------------------------------------------------- #
mainClock = pygame.time.Clock()
# Fonts ----------------------------------------------------------- #
fps_font = pygame.font.SysFont("Silver.ttf", 22)
# Music ----------------------------------------------------------- #
pygame.mixer.music.load("Assets/Sounds/background.mp3")
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)

# Game ----------------------------------------------------------- #
game = Game(SCREEN)


# events ----------------------------------------------------------- #
def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


# update ----------------------------------------------------------- #
def update():
    enemy_handle.update(SCREEN)
    scroll_bar.update(SCREEN, enemy_handle, hand, game, ball)
    pygame.display.update()
    mainClock.tick(FPS)


# draw ------------------------------------------------------------- #
def draw(surface):
    # draw lane
    lane[0].draw_lane(surface)
    lane[1].draw_lane(surface)
    lane[2].draw_lane(surface)



# statement -------------------------------------------------------- #
# scroll_bar
scroll_bar = ScrollBar()
# lane
lane = [
    Lane(LANE_X, LANE_Y),
    Lane(LANE_X, LANE_Y + LANE_VEL),
    Lane(LANE_X, LANE_Y + LANE_VEL * 2)
]
# hand
hand = Hand()
# enemy
enemy = Enemy()
# enemy handle


enemy_handle = EnemyHandle()
# ball TODO 新增
ball = pygame.sprite.GroupSingle()

# Loop ------------------------------------------------------------ #
while True:
    user_events()
    SCREEN.fill((255, 255, 255))


    draw(SCREEN)

    update()
    # 更新屏幕显示
    pygame.display.flip()
    # FPS
    if DRAW_FPS:
        fps_label = fps_font.render(f"FPS: {int(mainClock.get_fps())}",
                                    1, (255, 200, 20))
        SCREEN.blit(fps_label, (5, 5))
