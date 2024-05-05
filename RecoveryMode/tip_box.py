import time

import pygame.draw
import re
import image
from settings import *


class TipBox:
    def __init__(self, surface, gesture):
        self.surface = surface
        self.gesture = gesture
        self.pattern = r'\b([\w-]+)\.png\b'
        self.gesture_image = image.load(f'Assets/gesture/{self.gesture.get_selected_gesture_name()}', size=TIP_BOX_SIZE)
        # 利用正则表达式去除.png 从而得到图片名 进而判断手势是否符合
        self.gesture_image_name = re.search(self.pattern, self.gesture.get_selected_gesture_name(),
                                            re.IGNORECASE).group(1)
        self.gesture_image_rect = self.gesture_image.get_rect(topleft=exhibit_pos)
        self.right_image = image.load('Assets/tipbox/right.png', size=TIP_BOX_SIZE)
        self.right_image_rect = self.right_image.get_rect(topleft=TIP_BOX_POS)
        self.wrong_image = image.load('Assets/tipbox/wrong.png', size=TIP_BOX_SIZE)
        self.wrong_image_rect = self.wrong_image.get_rect(topleft=TIP_BOX_POS)
        self.image = self.wrong_image
        self.image_rect = self.wrong_image_rect

    def set_image(self):
        self.gesture_image = image.load(f'Assets/gesture/{self.gesture.get_selected_gesture_name()}', size=TIP_BOX_SIZE)
        self.gesture_image_rect = self.gesture_image.get_rect(topleft=exhibit_pos)
        self.gesture_image_name = re.search(self.pattern, self.gesture.get_selected_gesture_name(),
                                            re.IGNORECASE).group(1)

    def draw(self):
        self.surface.blit(self.gesture_image, self.gesture_image_rect)
        self.surface.blit(self.image, self.image_rect)

    def change_pass_image(self, flag):
        if flag:
            self.image = self.right_image
            self.image_rect = self.right_image_rect
        else:
            self.image = self.wrong_image
            self.image_rect = self.wrong_image_rect

    def update(self):
        self.set_image()
        self.draw()
