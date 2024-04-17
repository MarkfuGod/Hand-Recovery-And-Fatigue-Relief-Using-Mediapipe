import pygame
import random
import image
from card import Card
import settings


class ScrollBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 滚动条图片
        self.scroll_image = image.load("Assets/scroll_bar/scroll_bar.png", size=settings.SCROLL_BAR_SIZES)
        # 滚动条矩形
        self.scroll_rect = self.scroll_image.get_rect(center=(600, 80))
        # 传送带中种类卡片的数量
        self.fire_num = random.randint(5, 10)
        self.ground_num = random.randint(5, 7)
        self.ice_num = random.randint(3, 6)
        self.golden_num = random.randint(4, 8)
        # 滚动条中卡片列表
        self.card_list = pygame.sprite.Group()
        # card_list中最后添加卡片的时间
        self.last_added_time = pygame.time.get_ticks()
        # card_list中添加时间的时间间隔   随机化
        self.add_card_interval = random.randint(2000, 5000)  # Randomize the initial interval

    def try_add_card(self):
        """
        尝试添加新卡片到卡片列表中，根据条件选择卡片类型并设置位置间隔。
        :param 无
        :return 无
        """
        current_time = pygame.time.get_ticks()
        if len(self.card_list) < 10 and current_time - self.last_added_time > self.add_card_interval:
            # 定义卡片类型列表
            card_types = ["card_ice", "card_fire", "card_golden", "card_ground"]
            # 定义每种卡片的数量
            ice_count = 0
            fire_count = 0
            golden_count = 0
            ground_count = 0
            # 检查每种卡片的数量是否已经达到规定的值
            for card_type in card_types:
                if card_type == "card_ice" and ice_count >= self.ice_num:
                    card_types.remove("card_ice")
                elif card_type == "card_fire" and fire_count >= self.fire_num:
                    card_types.remove("card_fire")
                elif card_type == "card_golden" and golden_count >= self.golden_num:
                    card_types.remove("card_golden")
                elif card_type == "card_ground" and ground_count >= self.ground_num:
                    card_types.remove("card_ground")
            # 如果所有的卡片都到了规定的值，就不再添加
            if not card_types:
                return
            # 随机选择一种卡片类型
            selected_type = random.choice(card_types)
            if selected_type == "card_ice":
                ice_count += 1
            elif selected_type == "card_fire":
                fire_count += 1
            elif selected_type == "card_golden":
                golden_count += 1
            elif selected_type == "card_ground":
                ground_count += 1
            # 使用随机选择的卡片类型创建卡片
            self.add_card(Card(selected_type))
            self.last_added_time = current_time
            self.add_card_interval = random.randint(2000, 5000)  # Randomize the interval for the next card

    def add_card(self, card):
        """
        向卡片列表中添加卡片，并根据上一个卡片的位置设置新卡片的位置。
        :param card: 要添加的卡片对象
        :return 无
        """
        self.card_list.add(card)
        last_card = None
        max_right = 0
        for c in self.card_list:
            if c.card_rect.right > max_right:
                max_right = c.card_rect.right
                last_card = c
        if last_card and last_card != card:
            # 在最后一张卡片的右侧随机距离处放置新卡片，以避免重叠
            card.card_rect.x = max_right + random.randint(50, 150)

    def add_card1(self, card):
        """
        向卡片列表中添加卡片，并根据上一个卡片的位置设置新卡片的位置。
        :param card: 要添加的卡片对象
        :return 无
        """
        self.card_list.add(card)
        # last_card = None
        max_right = 0
        for c in self.card_list:
            if c.card_rect.right > max_right:
                max_right = c.card_rect.right
                # last_card = c

        card.card_rect.x = 100
        card.card_rect.y = 20

    def update(self, surface, enemy_handle, hand, game, ball_handle, lane):
        """
        更新滚动条，包括尝试添加新卡片和处理卡片之间的碰撞。
        :param 无
        :return 无
        """
        self.try_add_card()
        self.draw(surface)
        for card in self.card_list:
            card.update(self.scroll_rect, surface, enemy_handle)
            for other_card in self.card_list:
                if card != other_card and card.card_rect.colliderect(other_card.card_rect) and not other_card.moving:
                    card.moving = False
        # game.update(self.card_list)
        game.update(self.card_list, ball_handle, surface, lane, enemy_handle, self)

    def permit_moving_after_release(self):
        for card in self.card_list:
            if card.rect.left == self.scroll_rect.left:
                return True
        return False

    # def draw(self, surface):
    #     """
    #     在表面上绘制滚动条和所有卡片。
    #     :param surface: 要绘制的表面
    #     :return 无
    #     """
    #     surface.blit(self.scroll_image, self.scroll_rect)
    #     for card in self.card_list:
    #         card.draw(surface, self.scroll_rect)
    def draw(self, surface):
        """
        在表面上绘制滚动条和所有卡片。
        :param surface: 要绘制的表面
        :return 无
        """
        surface.blit(self.scroll_image, self.scroll_rect)
        # 判断卡片是否重叠，如果重叠后一个卡片等于前一个卡片向后移动5px
        for card1 in self.card_list:
            if not self.permit_moving_after_release():
                card1.moving = True
            for card2 in self.card_list:
                if card1 != card2 and card1.rect.colliderect(card2.rect):
                    card2.rect.left = card1.rect.right + 5

        for card in self.card_list:
            card.draw(surface, self.scroll_rect)
