import pygame

from ball import Ball
from hand_tracking import HandTracking
from hand import Hand
from scroll_bar import ScrollBar
from card import Card


class Drag:
    def __init__(self):
        # self.hand_tracking = hand_tracking
        self.is_draw = False
        self.which_card = ""

    def update(self, hand, card_list, ball_handle, surface, lane, hand_tracking):
        # self.is_draw=False
        # print("drag")
        # print(hand.is_hand_closed())
        # 检查手是否闭合
        if hand_tracking.hand_closed:
            # print(hand_tracking.hand_closed)
            # 遍历所有卡片，检查是否与手的位置重叠
            for card in card_list:
                if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_ice":
                    # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                    card.card_rect.center = hand.rect.center
                    card.move = True  # 标记卡片为移动状态
        if hand_tracking.two_fingers_up:
            # print("拖动")
            # 遍历所有卡片，检查是否与手的位置重叠
            for card in card_list:
                if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_fire":
                    # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                    card.card_rect.center = hand.rect.center
                    card.move = True  # 标记卡片为移动状态
        if hand_tracking.thumb_up:
            # print("拖动")
            # 遍历所有卡片，检查是否与手的位置重叠
            for card in card_list:
                if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_golden":
                    # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                    card.card_rect.center = hand.rect.center
                    card.move = True  # 标记卡片为移动状态
        if hand_tracking.finger_up:
            # print("拖动")
            # 遍历所有卡片，检查是否与手的位置重叠
            for card in card_list:
                if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_ground":
                    # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                    card.card_rect.center = hand.rect.center
                    card.move = True  # 标记卡片为移动状态
        else:
            # 如果手不是闭合状态，释放所有正在移动的卡片
            for card in card_list:
                if card.move:
                    # 检查卡片是否与(200, 155)点碰撞
                    if card.rect.collidepoint((230, 230)):
                        self.which_card = card.get_card_type()
                        self.is_draw = True
                        card.move = False  # 标记卡片为非移动状态
                        card.kill()
                        # 设置ball的起始位置为(200, 155)
                        if not card.has_used:
                            card.ball.rect.center = (230, 230)
                            ball_handle.ball_list.add(card.ball)
                            card.has_used = True
                    elif card.rect.collidepoint((230, 400)):
                        self.which_card = card.get_card_type()
                        self.is_draw = True
                        card.move = False  # 标记卡片为非移动状态
                        card.kill()
                        # 设置ball的起始位置为(200, 155)
                        if not card.has_used:
                            card.ball.rect.center = (230, 400)
                            ball_handle.ball_list.add(card.ball)
                            card.has_used = True
                    elif card.rect.collidepoint((230, 550)):
                        self.which_card = card.get_card_type()
                        self.is_draw = True
                        card.move = False  # 标记卡片为非移动状态
                        card.kill()
                        # 设置ball的起始位置为(200, 155)
                        if not card.has_used:
                            card.ball.rect.center = (230, 550)
                            ball_handle.ball_list.add(card.ball)
                            card.has_used = True
        return self.which_card, self.is_draw
