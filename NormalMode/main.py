# Setup Python ----------------------------------------------- #
import pygame
import sys
import os
from settings import *
from enemy import *

# from game import Game
# from menu import Menu
# Setup pygame/window --------------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 32)  # windows position
pygame.init()
pygame.display.set_caption(WINDOW_NAME)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

mainClock = pygame.time.Clock()
# Fonts ----------------------------------------------------------- #
fps_font = pygame.font.SysFont("Silver.ttf", 22)


# Music ----------------------------------------------------------- #
# pygame.mixer.music.load("Assets/Sounds/background.mp3")
# pygame.mixer.music.set_volume(MUSIC_VOLUME)
# pygame.mixer.music.play(-1)

def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def update():
    pygame.display.update()
    mainClock.tick(FPS)


lane = pygame.image.load("Assets/floor1.png")
lane_rec_1 = lane.get_rect(topleft=(285, 240))
lane_rec_2 = lane.get_rect(topleft=(285, 473))
lane_rec_3 = lane.get_rect(topleft=(285, 706))
enemy = Enemy()
enemy_handle = EnemyHandle()
# Loop ------------------------------------------------------------ #
while True:
    user_events()

    SCREEN.fill((255, 255, 255))
    SCREEN.blit(lane, lane_rec_1)
    SCREEN.blit(lane, lane_rec_2)
    SCREEN.blit(lane, lane_rec_3)

    enemy_handle.update(SCREEN)

    # 更新屏幕显示
    pygame.display.flip()
    # FPS
    if DRAW_FPS:
        fps_label = fps_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255, 200, 20))
        SCREEN.blit(fps_label, (5, 5))
