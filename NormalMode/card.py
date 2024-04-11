import pygame
import image


class Card(pygame.sprite.Sprite):
    def __init__(self, card_type):
        super().__init__()
        # 加载图片
        self.card_fire = image.load("Assets/scroll_bar/card_fire.png")
        self.card_golden = image.load("Assets/scroll_bar/card_golden.png")
        self.card_ice = image.load("Assets/scroll_bar/card_ice.png")
        self.card_ground = image.load("Assets/scroll_bar/card_ground.png")
        # 卡片元素
        self.type = card_type
        if self.type == "card_ice":
            # 设置默认图像
            self.image = self.card_ice
            # 设置默认位置
            self.card_rect = self.image.get_rect(topleft=(1800, 30))
        if self.type == "card_fire":
            self.image = self.card_fire
            self.card_rect = self.image.get_rect(topleft=(1800, 30))
        if self.type == "card_golden":
            self.image = self.card_golden
            self.card_rect = self.image.get_rect(topleft=(1800, 30))
        if self.type == "card_ground":
            self.image = self.card_ground
            self.card_rect = self.image.get_rect(topleft=(1800, 30))
        # 卡片移动速度
        self.card_speed = 2
        self.rect = self.card_rect
        # 标记卡片是否应该继续移动
        self.moving = True
        # 标记卡片是否被释放
        self.released = False
        self.effected_by_card_ground = True

    def update(self, scroll_rect,surface,enemy_handle):
        # 如果卡片没有被释放
        if not self.released:
            self.draw(surface,scroll_rect)

            if self.moving:
                self.card_rect.x -= self.card_speed
                if self.card_rect.x < scroll_rect.left:  # 如果卡片移动到scroll_rect的左侧
                    self.card_rect.x = scroll_rect.left  # 停止移动
                    self.moving = False
        else:
            enemy_handle.enemy_enchanted_handle(self)
            # 被释放那就从传送带中删除
            self.draw(surface,scroll_rect)
            self.move_right()
            pass

    def draw(self, surface, scroll_rect):
        if not self.released:
            if self.card_rect.right > scroll_rect.left + 10:  # Adjusted to not cover the scroll bar border
                visible_part = self.card_rect.clip(scroll_rect)
                visible_part_relative = visible_part.move(-self.card_rect.x, -self.card_rect.y)
                surface.blit(self.image, visible_part, area=visible_part_relative)
        else:
            surface.blit(self.image, (self.card_rect.x, self.card_rect.y))

    def move_right(self):
        # 增加卡片移动速度到当前位置
        self.card_rect.x += self.card_speed
        # 注意：这里我们只移动self.rect的x值，因为draw方法中的位置是基于self.rect.x计算的

    def get_card_type(self):
        return self.type

    def clear_image(self):
        # 假设image_to_clear是一个pygame.Surface对象
        self.kill()  # 使用透明颜色填充图像
