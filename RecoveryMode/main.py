# Setup Python ----------------------------------------------- #
import sys
import os

from image import *
from settings import *
from hand_tracking import *
import game
import button

# from menu import Menu
# Setup pygame/window --------------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 32)  # windows position
pygame.init()
pygame.display.set_caption(WINDOW_NAME)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF, 32)
mainClock = pygame.time.Clock()
# Fonts ----------------------------------------------------------- #
fps_font = pygame.font.SysFont("Silver.ttf", 22)

# Music ----------------------------------------------------------- #
# pygame.mixer.music.load("Assets/Sounds/background.mp3")
# pygame.mixer.music.set_volume(MUSIC_VOLUME)
# pygame.mixer.music.play(-1)

# Statement ------------------------------------------------------- #
game_paused = False
game = game.Game(SCREEN)
handtracking = HandTracking()
# Todo
button_pause = button.Button("pause")
button_return = button.Button("return")
button_next = button.Button("next")
button_mute = button.Button("mute")


def user_events():
    global game_paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_pause.rect.collidepoint(event.pos):
                if game_paused:
                    # If the game is already paused, clicking the button resumes the game
                    game_paused = False
                    print("Game resumed!")
                else:
                    # If the game is not paused, clicking the button pauses the game
                    game_paused = True
                    print("Game paused!")
            elif button_return.rect.collidepoint(event.pos):
                print("Return button clicked!")
                pygame.quit()
                sys.exit()
            # Todo
            elif button_next.rect.collidepoint(event.pos):
                print("Next Gesture button clicked!")
                game.next_gesture()


def update():
    pygame.display.update()
    mainClock.tick(FPS)


def draw_buttons():
    button_pause.draw_button(SCREEN)
    button_return.draw_button(SCREEN)
    button_next.draw_button(SCREEN)
    button_mute.draw_button(SCREEN)

SCREEN.blit(background, background_rect)
SCREEN.blit(video_background,video_back_rect)
SCREEN.blit(bar,bar_rect)
# Loop ------------------------------------------------------------ #
while True:

    user_events()
    draw_buttons()
    # If the game is paused, don't update the screen or process other game logic

    if not game_paused:
        # 更新滚动条
        update()
        game.update()
        # 更新屏幕显示
        pygame.display.flip()
    else:
        # While the game is paused, we can handle other things, like waiting for events
        pygame.time.Clock().tick(10)  # 这使得pygame能够处理内部事件，但保持低帧率
    # FPS
    if DRAW_FPS:
        fps_label = fps_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255, 200, 20))
        SCREEN.blit(fps_label, (5, 5))
