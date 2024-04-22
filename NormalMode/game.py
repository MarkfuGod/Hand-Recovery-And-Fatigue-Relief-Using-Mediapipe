import time
import pygame

from NormalMode import end
from NormalMode.ball import BallHandle
from NormalMode.collision import Collision
from NormalMode.enemy import EnemyHandle
from drag import Drag
from hand import Hand
from hand_tracking import HandTracking
import cv2
from scroll_bar import ScrollBar
from settings import *


class Game:
    def __init__(self, surface, ball_handle, enemy_handle, scroll_bar):
        self.which_card = None
        self.frame = None
        self.is_draw = False
        self.gestures = []
        self.game_start_time = time.time()
        self.score = 0
        self.hand = Hand()
        self.hand_tracking = HandTracking()
        self.surface = surface
        self.scroll_bar = scroll_bar
        self.enemy_handle = enemy_handle
        self.ball_handle = ball_handle

        # Load camera
        self.cap = cv2.VideoCapture(0)
        # TODO 新增
        self.drag = Drag()

        self.collision=Collision()
        self.score = 0  # 添加分数属性

    def reset(self):  # reset all the needed variables
        self.hand_tracking = HandTracking()
        self.gestures = []
        self.score = 0
        self.game_start_time = time.time()
        self.ball_handle.reset()
        self.enemy_handle.reset()  # 重置敌人状态
        self.scroll_bar.reset()  # 重置滚动条状态
        self.surface.fill((255, 255, 255))

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)  # 选择合适的字体和大小
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))  # 创建分数文本
        self.surface.blit(score_text, (self.surface.get_width() - score_text.get_width() - 10,
                                       self.surface.get_height() - score_text.get_height() - 10))  # 将分数绘制到右下角
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

    def update(self, ball_handle, surface, lane, enemy_handle, scroll_bar):

        self.load_camera()
        self.set_hand_position()
        (x, y) = self.hand_tracking.get_hand_center()
        self.hand.rect.center = (x, y)
        self.hand.left_click = (
                self.hand_tracking.love is True or self.hand_tracking.six is True or self.hand_tracking.two_fingers_up
                is True or self.hand_tracking.finger_up is True)

        # TODO 新增
        self.which_card, self.is_draw = self.drag.update(self.hand, ball_handle, surface, lane,
                                                         self.hand_tracking, scroll_bar)
        ball_handle.update(surface)
        for ball in ball_handle.ball_list:
            self.collision.collide_with_element(ball,enemy_handle.enemy_list, self)
        scroll_bar.update(surface, enemy_handle, ball_handle)
        if enemy_handle.update(surface) == 1:
            end.show_victory_screen(surface, self)
        elif enemy_handle.update(surface) == -1:
            end.show_defeat_screen(surface, self)

        self.draw()

        if self.hand.left_click:
            self.hand.image = self.hand.image_smaller.copy()
        else:
            self.hand.image = self.hand.orig_image.copy()

        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)
