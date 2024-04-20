import pygame

from ball import Ball
from hand_tracking import HandTracking
from hand import Hand
from scroll_bar import ScrollBar
from card import Card


class Drag:
    def __init__(self):
        """
        is_draw: 是否生成球
        which_card: 拖拽的卡片类型
        """
        self.is_draw = False
        self.which_card = ""

    def update(self, hand, ball_handle, surface, lane, hand_tracking, scroll_bar):
        """
        更新拖拽状态
        """
        # 检查手是否闭合
        if hand.left_click:
            if hand_tracking.love:
                # 遍历所有卡片，检查是否与手的位置重叠
                for card in scroll_bar.card_list:
                    if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_ice":
                        # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                        card.card_rect.center = hand.rect.center
                        card.move = True  # 标记卡片为移动状态
                        card.is_drag = True
            if hand_tracking.two_fingers_up:
                # 遍历所有卡片，检查是否与手的位置重叠
                for card in scroll_bar.card_list:
                    if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_fire":
                        # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                        card.card_rect.center = hand.rect.center
                        card.move = True  # 标记卡片为移动状态
                        card.is_drag = True
            if hand_tracking.six:
                # 遍历所有卡片，检查是否与手的位置重叠
                for card in scroll_bar.card_list:
                    if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_golden":
                        # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                        card.card_rect.center = hand.rect.center
                        card.move = True  # 标记卡片为移动状态
                        card.is_drag = True
            if hand_tracking.finger_up:
                # 遍历所有卡片，检查是否与手的位置重叠
                for card in scroll_bar.card_list:
                    if card.rect.collidepoint(hand.rect.center) and card.get_card_type() == "card_ground":
                        # 如果手闭合且卡片与手重叠，更新卡片位置为手的位置
                        card.card_rect.center = hand.rect.center
                        card.move = True  # 标记卡片为移动状态
                        card.is_drag = True
        else:
            # 如果手不是闭合状态，释放所有正在移动的卡片
            for card in scroll_bar.card_list:
                card.is_drag = False
                if card.move:
                    # 检查卡片是否与(200, 155)点碰撞
                    if card.rect.collidepoint((200, 230)):
                        self.which_card = card.get_card_type()
                        self.is_draw = True
                        card.move = False  # 标记卡片为非移动状态
                        card.kill()
                        # 设置ball的起始位置为(200, 155)
                        if not card.has_used:
                            card.ball.rect.center = (200, 230)
                            ball_handle.ball_list.add(card.ball)
                            card.has_used = True
                    elif card.rect.collidepoint((200, 400)):
                        self.which_card = card.get_card_type()
                        self.is_draw = True
                        card.move = False  # 标记卡片为非移动状态
                        card.kill()
                        # 设置ball的起始位置为(200, 155)
                        if not card.has_used:
                            card.ball.rect.center = (200, 400)
                            ball_handle.ball_list.add(card.ball)
                            card.has_used = True
                    elif card.rect.collidepoint((200, 550)):
                        self.which_card = card.get_card_type()
                        self.is_draw = True
                        card.move = False  # 标记卡片为非移动状态
                        card.kill()
                        # 设置ball的起始位置为(200, 155)
                        if not card.has_used:
                            card.ball.rect.center = (200, 550)
                            ball_handle.ball_list.add(card.ball)
                            card.has_used = True
                    if not (card.rect.collidepoint((200, 230)) or card.rect.collidepoint(
                            (200, 400)) or card.rect.collidepoint((200, 550))):
                        # 如果没有重叠，将卡片返回到传送带上
                        card.move = False  # 停止卡片移动
                        scroll_bar.add_card1(card)  # 将卡片添加回传送带
        return self.which_card, self.is_draw
