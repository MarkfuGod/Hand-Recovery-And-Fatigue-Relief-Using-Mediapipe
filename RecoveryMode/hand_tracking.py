import math
import numpy as np
import cv2
import mediapipe as mp
from settings import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# TODO: Change the detection mode here to Gesture

def h_gesture(angle_list):
    """
        # 二维约束的方法定义手势
        每个手势都有一个特定的角度阈值，如果所有的角度都满足这个阈值，那么就认为是这个手势。
        # fist five gun love one six three thumbup yeah
    """
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
        if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "fist"
        # elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s)
        # and ( angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s): gesture_str = "five"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "gun"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "love"
        elif (angle_list[0] > 5) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "one"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "six"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (
                angle_list[2] < thr_angle_s) and (angle_list[3] < thr_angle_s) and (angle_list[4] > thr_angle):
            gesture_str = "three"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "thumbup"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (
                angle_list[2] < thr_angle_s) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "two"
    return gesture_str


def vector_2d_angle(v1, v2):
    """
        求解二维向量的角度
    """
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_


class HandTracking:
    def __init__(self):
        self.hand_tracking = mp_hands.Hands(static_image_mode=False,
                                            max_num_hands=1,
                                            model_complexity=1,
                                            min_detection_confidence=0.5,
                                            min_tracking_confidence=0.2)
        self.hand_x = 0
        self.hand_y = 0
        self.results = None
        self.love = False
        self.six = False
        self.three = False
        self.gun = False
        self.fist = False
        # self.thumb_down = False
        self.one = False
        self.two = False
        self.thumbup = False

    def hand_angle(self, hand_):
        """
            获取对应手相关向量的二维角度,根据角度确定手势
            这个角度是通过计算两个向量之间的角度得到的，这两个向量分别是从手腕到指关节的向量和从指关节到指尖的向量。
            计算出的每个角度都被添加到一个列表中，然后返回这个列表。
        """
        angle_list = []
        # ---------------------------- thumb 大拇指角度
        angle_ = vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
            ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- index 食指角度
        angle_ = vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
            ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- middle 中指角度
        angle_ = vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
            ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- ring 无名指角度
        angle_ = vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
            ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- pink 小拇指角度
        angle_ = vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
            ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
        )
        angle_list.append(angle_)
        return angle_list

    def scan_hands(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = self.hand_tracking.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.love = False
        self.six = False
        # self.thumb_down = False
        self.one = False
        self.two = False
        self.fist = False
        self.gun = False
        self.thumbup = False
        self.three = False

        if self.results.multi_hand_landmarks:
            gesture_strs = []
            avg_xs = []
            for hand_landmarks in self.results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # 获取关键点坐标
                # landmarks = hand_landmarks.landmark
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                self.hand_x = int(x * SCREEN_WIDTH)
                self.hand_y = int(y * SCREEN_HEIGHT)
                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x * image.shape[1]
                    y = hand_landmarks.landmark[i].y * image.shape[0]
                    hand_local.append((x, y))
                if hand_local:
                    angle_list = self.hand_angle(hand_local)
                    gesture_str = h_gesture(angle_list)
                    if gesture_str == 'love':
                        self.love = True
                    elif gesture_str == 'six':
                        self.six = True
                    elif gesture_str == 'one':
                        self.one = True
                    elif gesture_str == 'two':
                        self.two = True
                    elif gesture_str == 'three':
                        self.three =True
                    elif gesture_str == 'gun':
                        self.gun = True
                    elif gesture_str == 'thumbup':
                        self.thumbup = True
                    elif gesture_str == 'fist':
                        self.fist = True
                    gesture_strs.append(gesture_str)
                    # print(gesture_strs)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.rot90(image)
        image = pygame.surfarray.make_surface(image)
        return image

    def get_hand_center(self):
        return self.hand_x, self.hand_y

    def display_hand(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)

