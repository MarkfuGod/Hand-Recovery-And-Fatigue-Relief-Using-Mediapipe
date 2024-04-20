import pygame
import sys


def restart_game(game):
    game.reset()
    pass
    # 重新开始游戏的逻辑
    # 这里需要根据实际游戏逻辑来实现，可能包括重置游戏状态、分数等


def show_victory_screen(screen, game):
    background = pygame.image.load('Assets/background.png')  # 加载背景图片
    screen.blit(background, (0, 0))  # 将背景图片绘制到屏幕上
    font = pygame.font.SysFont(None, 55)
    text = font.render('Victory!', True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 350))
    screen.blit(text, text_rect)
    wait_for_restart(screen, game)


def show_defeat_screen(screen, game):
    background = pygame.image.load('Assets/background.png')  # 加载背景图片
    screen.blit(background, (0, 0))  # 将背景图片绘制到屏幕上
    font = pygame.font.SysFont(None, 55)
    text = font.render('Be Defeated!', True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 350))
    screen.blit(text, text_rect)
    wait_for_restart(screen, game)


def draw_button(screen, text, position, action=None):
    font = pygame.font.SysFont(None, 55)
    text_render = font.render(text, True, (255, 255, 255))
    text_rect = text_render.get_rect(center=position)
    button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
    pygame.draw.rect(screen, (0, 0, 0), button_rect)  # Draw button
    screen.blit(text_render, text_rect)
    return button_rect


def wait_for_restart(screen, game):
    restart_button = draw_button(screen, 'Restart', (screen.get_width() / 2, screen.get_height() / 2 + 100))
    pygame.display.flip()
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    restart_game(game)  # Assuming restart_game is properly defined to reset the game
                    flag = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                flag = False
