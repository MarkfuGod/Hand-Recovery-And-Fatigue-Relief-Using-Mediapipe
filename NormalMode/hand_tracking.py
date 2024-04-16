import cv2
import mediapipe as mp
from settings import *
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# TODO: Change the detection mode here to Gesture

class HandTracking:
    def __init__(self):
        self.hand_tracking = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.hand_x = 0
        self.hand_y = 0
        self.results = None
        self.hand_closed = False
        self.thumb_up = False
        # self.thumb_down = False
        self.finger_up = False
        self.two_fingers_up = False

    def scan_hands(self, image):
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = self.hand_tracking.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.hand_closed = False
        self.thumb_up = False
        # self.thumb_down = False
        self.finger_up = False
        self.two_fingers_up = False

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # 获取关键点坐标
                landmarks = hand_landmarks.landmark
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                self.hand_x = int(x * SCREEN_WIDTH)
                self.hand_y = int(y * SCREEN_HEIGHT)
                # 修改握拳判断逻辑：只需要判断除了大拇指外其他四个手指握下就判断为握拳    hand_closed
                finger_tips = [8, 12, 16, 20]  # 食指到小指的指尖landmark索引
                finger_folded = [landmarks[finger_tip].y > landmarks[finger_tip - 2].y for finger_tip in finger_tips]
                self.hand_closed = all(finger_folded)

                # 修改拇指朝上判断逻辑   thumb_up
                # 拇指朝上且其他手指握拳
                if landmarks[4].y < landmarks[3].y and all(finger_folded[1:]):  # 修正逻辑，确保其他手指握拳
                    self.thumb_up = True

                # 新增识别数字二手势的代码  two_fingers_up
                # 数字二手势：食指和中指伸直，无名指和小拇指弯曲
                if landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and all(landmarks[finger_tip].y > landmarks[finger_tip - 2].y for finger_tip in [16, 20]):
                    self.two_fingers_up = True  # 添加一个新的属性来表示数字二手势

                # # 拇指朝下判断
                # if landmarks[4].y > landmarks[3].y > landmarks[2].y and landmarks[8].y > landmarks[6].y:
                #     self.thumb_down = True

                # 只有食指没弯曲判断 finger_up
                if landmarks[8].y < landmarks[6].y and all(landmarks[finger_tip].y > landmarks[finger_tip - 2].y for finger_tip in [12, 16, 20]):
                    self.finger_up = True

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        return image

    def get_hand_center(self):
        return self.hand_x, self.hand_y

    def display_hand(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)
    #
    # def card_follow_hand(self, card):
    #     if self.hand_closed:
    #         if card.rect.collidepoint(self.hand_x, self.hand_y):
    #             card.rect.center = self.get_hand_center()
    #             card.moving = False
