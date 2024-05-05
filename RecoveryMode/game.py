import pygame
import time
import random
from settings import *
from hand_tracking import HandTracking
import cv2
import ui
from gesture import *
from tip_box import *


class Game:
    def __init__(self, surface):
        self.surface = surface
        # self.background = Background()
        self.hand_tracking = HandTracking()
        # Load camera
        self.cap = cv2.VideoCapture(0)

        self.sounds = {}
        self.sounds["slap"] = pygame.mixer.Sound(f"Assets/Sounds/slap.wav")
        self.sounds["slap"].set_volume(SOUNDS_VOLUME)
        self.sounds["screaming"] = pygame.mixer.Sound(f"Assets/Sounds/screaming.wav")
        self.sounds["screaming"].set_volume(SOUNDS_VOLUME)
        self.gesture = Gesture()
        self.tip_box = TipBox(surface, self.gesture)
        self.index=0

    def reset(self):  # reset all the needed variables
        self.hand_tracking = HandTracking()
        # self.hand = Hand()
        # self.score = 0
        # self.game_start_time = time.time()

    def set_hand_position(self):
        self.frame = self.hand_tracking.scan_hands(self.frame)
        (x, y) = self.hand_tracking.get_hand_center()
        resized_frame = pygame.transform.scale(self.frame, (700,400))
        self.surface.blit(resized_frame, (300,200))
        pygame.display.flip()

    def load_camera(self):
        _, self.frame = self.cap.read()

    # 判断用户做出的手势是否正确 为防止特殊情况 默认值返回 False
    def is_gesture_true(self):
        if getattr(self.hand_tracking, self.tip_box.gesture_image_name, False):
            return True
        else:
            return False

    def update(self):
        self.load_camera()
        self.set_hand_position()
        cv2.waitKey(1)
        self.gesture.update(self.surface, self.index)
        self.tip_box.update()
        if self.is_gesture_true():
            self.index=self.index+1
        self.tip_box.change_pass_image(self.is_gesture_true())

    def next_gesture(self):
        self.index = self.index + 1

