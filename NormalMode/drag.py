import pygame

from NormalMode.ball import Ball
from hand_tracking import HandTracking
from hand import Hand
from scroll_bar import ScrollBar
from card import Card

class Drag:
    def __init__(self):
        # self.hand_tracking = hand_tracking
        self.is_draw=False
        self.which_card=""

    def update(self,hand,card_list,ball,surface):
        # self.is_draw=False
        print("drag")
        print(hand.is_hand_closed())
        # 检查手是否闭合
        if hand.is_hand_closed():
            print("拖动")
            # 遍历所有卡片，检查是否与手的位置重叠
            for card in card_list:
                if card.rect.collidepoint(hand.rect.center):
                    # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                    card.card_rect.center = hand.rect.center
                    card.move = True  # 标记卡片为移动状态
        else:
            # 如果手不是闭合状态，释放所有正在移动的卡片
            for card in card_list:
                if card.move:
                    self.which_card=card.get_card_type()
                    self.is_draw=True
                    # ball.draw(surface)
                    card.move = False  # 标记卡片为非移动状态
        return self.which_card,self.is_draw

