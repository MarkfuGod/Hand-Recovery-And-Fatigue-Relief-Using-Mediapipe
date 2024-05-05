# three buttons
# 1: button pause
# 2: button return
# 3: button next gesture
# 4: button mute
import pygame
from settings import *
import image


class Button:

    # size: size of button
    def __init__(self, button_type):
        self.button_type = button_type
        if button_type == "pause":
            self.rect = pygame.Rect(BUTTON_PAUSE_POSITION, BUTTONS_SIZES)
            self.image = image.scale(image.load("Assets/button/pause.png"), BUTTONS_SIZES)
        elif button_type == "return":
            self.rect = pygame.Rect(BUTTON_RETURN_POSITION, BUTTONS_SIZES)
            self.image = image.scale(image.load("Assets/button/return.png"), BUTTONS_SIZES)
        elif button_type == "next":
            self.rect = pygame.Rect(BUTTON_NEXT_POSITION, BUTTONS_SIZES)
            self.image = image.scale(image.load("Assets/button/next.png"), BUTTONS_SIZES)
        elif button_type == "mute":
            self.rect = pygame.Rect(BUTTON_MUTE_POSITION, BUTTONS_SIZES)
            self.image = image.scale(image.load("Assets/button/sound.png"), BUTTONS_SIZES)

    def draw_button(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)

