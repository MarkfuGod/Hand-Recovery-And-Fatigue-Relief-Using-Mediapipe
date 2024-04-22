import pygame
import image
from settings import CARD_SIZES
from hand import Hand
from hand_tracking import HandTracking
from ball import Ball


class Card(pygame.sprite.Sprite):
    def __init__(self, card_type):
        super().__init__()
        # 加载图片
        self.card_fire = image.load("Assets/scroll_bar/card_fire.png", size=CARD_SIZES)
        self.card_golden = image.load("Assets/scroll_bar/card_golden.png", size=CARD_SIZES)
        self.card_ice = image.load("Assets/scroll_bar/card_ice.png", size=CARD_SIZES)
        self.card_ground = image.load("Assets/scroll_bar/card_ground.png", size=CARD_SIZES)
        # 卡片元素
        self.type = card_type
        self.hand_tracking = HandTracking()
        self.hand = Hand()
        '''
        image 卡片图片
        card_rect  卡片碰撞框
        gestureStatus 卡片相应元素对应的手势识别状态
        '''
        if self.type == "card_ice":
            self.image = self.card_ice
            self.card_rect = self.image.get_rect(topleft=(1200, 20))
            self.gestureStatus = self.hand_tracking.love
        if self.type == "card_fire":
            self.image = self.card_fire
            self.card_rect = self.image.get_rect(topleft=(1200, 20))
            self.gestureStatus = self.hand_tracking.two_fingers_up
        if self.type == "card_golden":
            self.image = self.card_golden
            self.card_rect = self.image.get_rect(topleft=(1200, 20))
            self.gestureStatus = self.hand_tracking.six
        if self.type == "card_ground":
            self.image = self.card_ground
            self.card_rect = self.image.get_rect(topleft=(1200, 20))
            self.gestureStatus = self.hand_tracking.finger_up
        # 卡片移动速度
        # FIXME 暂改,原为2
        self.card_speed = 10
        self.rect = self.card_rect
        # 标记卡片是否应该继续移动
        self.moving = True
        # 标记卡片是否被释放
        self.released = False
        self.effected_by_card_ground = True
        # TODO 新增
        self.selected = True
        self.move = False
        self.ball = Ball(self.type)
        self.has_used = False
        self.is_drag = False

    def update(self, scroll_rect, surface, enemy_handle):
        # 如果卡片没有被选中
        if not self.released:
            self.draw(surface, scroll_rect)
            if self.moving:
                self.card_rect.x -= self.card_speed
                if self.card_rect.x < scroll_rect.left:  # 如果卡片移动到scroll_rect的左侧
                    self.card_rect.x = scroll_rect.left  # 停止移动
                    self.moving = False
        else:
            enemy_handle.enemy_enchanted_handle(self)
            # 被释放那就从传送带中删除
            self.draw(surface, scroll_rect)

    def draw(self, surface, scroll_rect):
        if not self.released:
            if self.card_rect.right > scroll_rect.left + 10:  # Adjusted to not cover the scroll bar border
                visible_part = self.card_rect.clip(scroll_rect)
                visible_part_relative = visible_part.move(-self.card_rect.x, -self.card_rect.y)
                surface.blit(self.image, visible_part, area=visible_part_relative)
        surface.blit(self.image, (self.card_rect.x, self.card_rect.y))

    def get_card_type(self):
        return self.type

    def clear_image(self):
        # 假设image_to_clear是一个pygame.Surface对象
        self.kill()  # 使用透明颜色填充图像
