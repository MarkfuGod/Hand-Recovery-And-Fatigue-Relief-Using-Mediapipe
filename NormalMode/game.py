import pygame
import time
import random

from NormalMode.collision import Collision
from ball import Ball
from drag import Drag
from settings import *
from hand import Hand
from hand_tracking import HandTracking
import cv2
from scroll_bar import ScrollBar
import ui


class Game:
    def __init__(self, surface):
        self.is_draw = False
        self.gestures = []
        self.game_start_time = time.time()
        self.score = 0
        self.hand = Hand()
        self.hand_tracking = HandTracking()
        self.surface = surface
        self.scroll_bar = ScrollBar()

        # Load camera
        self.cap = cv2.VideoCapture(0)
        # TODO 新增
        self.drag = Drag()
        self.collision=Collision()

    def reset(self):  # reset all the needed variables
        self.hand_tracking = HandTracking()
        self.scroll_bar = ScrollBar()
        self.hand = Hand()
        self.gestures = []
        self.score = 0
        self.game_start_time = time.time()

    def load_camera(self):
        _, self.frame = self.cap.read()

    def set_hand_position(self):
        self.frame = self.hand_tracking.scan_hands(self.frame)
        (x, y) = self.hand_tracking.get_hand_center()
        self.hand.rect.center = (x, y)

    def draw(self):
        # draw the hand
        self.hand.draw(self.surface)
        # # draw the score
        # ui.draw_text(self.surface, f"Score : {self.score}", (5, 5), COLORS["score"], font=FONTS["medium"],
        #              shadow=True, shadow_color=(255, 255, 255))
        # # draw the time left
        # timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS[
        #     "timer"]  # change the text color if less than 5 s left
        # ui.draw_text(self.surface, f"Time left : {self.time_left}", (SCREEN_WIDTH // 2, 5), timer_text_color,
        #              font=FONTS["medium"],
        #              shadow=True, shadow_color=(255, 255, 255))

    def update(self, card_list, ball_handle, surface, lane,enemy_handle,scroll_ball):

        self.load_camera()
        self.set_hand_position()
        self.draw()

        (x, y) = self.hand_tracking.get_hand_center()
        self.hand.rect.center = (x, y)
        self.hand.left_click = (
                self.hand_tracking.love is True or self.hand_tracking.six is True or self.hand_tracking.two_fingers_up is True or self.hand_tracking.finger_up is True)
        # print("thumb_up", self.hand.left_click)
        # print("two_fingers_up", self.hand.left_click)
        # print("hand_closed", self.hand.left_click)
        # print("finger_up", self.hand.left_click)
        # TODO 新增
        self.which_card, self.is_draw = self.drag.update(self.hand, card_list, ball_handle, surface, lane,self.hand_tracking,scroll_ball)
        print("is_draw" + str(self.is_draw))
        # if self.is_draw:
        ball_handle.update(surface)
        for ball in ball_handle.ball_list:
            self.collision.collide_with_element(ball,enemy_handle.enemy_list)

        if self.hand.left_click:
            self.hand.image = self.hand.image_smaller.copy()
        else:
            self.hand.image = self.hand.orig_image.copy()

        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)
