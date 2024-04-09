import pygame
import random
import image

class Card(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__();
        card_fire = image.load("Assets/scroll_bar/card_fire.png")
        card_golden = image.load("Assets/scroll_bar/card_golden.png")
        card_ice = image.load("Assets/scroll_bar/card_ice.png")
        card_ground = image.load("Assets/scroll_bar/card_ground.png")
        self.card_images = [card_fire, card_golden, card_ice, card_ground]
        self.card_index = random.randint(0, len(self.card_images) - 1)  # 随机选择一张卡片
        self.card_speed = 1
        self.card = self.card_images[self.card_index]
        self.card_rect = self.card.get_rect(topleft=(1800, 30))  # 获取卡片的矩形区域
        self.moving = True  # 标记卡片是否应该继续移动

    def update(self, scroll_rect):
        if self.moving:
            self.card_rect.x -= self.card_speed
            if self.card_rect.x < scroll_rect.left:  # 如果卡片移动到scroll_rect的左侧
                self.card_rect.x = scroll_rect.left  # 停止移动
                self.moving = False

    def draw(self, surface, scroll_rect):
        if self.card_rect.right > scroll_rect.left + 10:  # Adjusted to not cover the scroll bar border
            visible_part = self.card_rect.clip(scroll_rect)
            visible_part_relative = visible_part.move(-self.card_rect.x, -self.card_rect.y)
            surface.blit(self.card, visible_part, area=visible_part_relative)

class ScrollBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.scroll_image = image.load("Assets/scroll_bar/scroll_bar.png")
        self.scroll_rect = self.scroll_image.get_rect(center=(900, 120))
        self.card_list = pygame.sprite.Group()
        self.last_added_time = pygame.time.get_ticks()
        self.add_card_interval = random.randint(2000, 5000)  # Randomize the initial interval

    def try_add_card(self):
        current_time = pygame.time.get_ticks()
        if len(self.card_list) < 10 and current_time - self.last_added_time > self.add_card_interval:  
            self.add_card(Card())
            self.last_added_time = current_time
            self.add_card_interval = random.randint(2000, 5000)  # Randomize the interval for the next card

    def add_card(self, card):
        self.card_list.add(card)
        last_card = None
        for c in self.card_list:
            if not last_card or c.card_rect.right > last_card.card_rect.right:
                last_card = c
        if last_card and last_card != card:
            # Randomize the distance for the new card from the last card
            card.card_rect.x = last_card.card_rect.right + random.randint(50, 150)

    def update(self):
        self.try_add_card()
        for card in self.card_list:
            card.update(self.scroll_rect)
            for other_card in self.card_list:
                if card != other_card and card.card_rect.colliderect(other_card.card_rect) and not other_card.moving:
                    card.moving = False

    def draw(self, surface):
        surface.blit(self.scroll_image, self.scroll_rect)
        for card in self.card_list:
            card.draw(surface, self.scroll_rect)