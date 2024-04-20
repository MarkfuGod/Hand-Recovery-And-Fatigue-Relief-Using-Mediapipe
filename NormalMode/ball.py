import pygame

import image
from settings import BALL_SIZE


class Ball(pygame.sprite.Sprite):
    def __init__(self, card_type):
        """
        初始化球类
        """
        super().__init__()
        # 在游戏设置区域定义移动速度
        self.card_move_speed = 5
        self.card_fire = image.load("Assets/ball/fire.png", size=BALL_SIZE)
        self.card_golden = image.load("Assets/ball/golden.png", size=BALL_SIZE)
        self.card_ice = image.load("Assets/ball/ice.png", size=BALL_SIZE)
        self.card_ground = image.load("Assets/ball/ground.png", size=BALL_SIZE)
        self.type = card_type  # 添加type属性
        self.effected_by_card_ground = True
        if self.type == "card_ice":
            self.image = self.card_ice  # 设置默认图像
            self.rect = self.image.get_rect(topleft=(320, 240))  # 设置默认位置
        if self.type == "card_fire":
            self.image = self.card_fire  # 设置默认图像
            self.rect = self.image.get_rect(topleft=(320, 240))  # 设置默认位置
        if self.type == "card_golden":
            self.image = self.card_golden  # 设置默认图像
            self.rect = self.image.get_rect(topleft=(320, 240))  # 设置默认位置
        if self.type == "card_ground":
            self.image = self.card_ground  # 设置默认图像
            self.rect = self.image.get_rect(topleft=(320, 240))  # 设置默认位置

    def draw(self, surface):
        """
        绘制球
        """
        surface.blit(self.image, self.rect)


    def move_right(self):
        """
        移动球
        """
        # 增加卡片移动速度到当前位置
        self.rect.x += 5
        print("------------------------------")
        print(str(self.card_move_speed))
        print("移动" + str(self.rect.x))
        print("------------------------------")
        # 注意：这里我们只移动self.rect的x值，因为draw方法中的位置是基于self.rect.x计算的

    def get_card_type(self):
        """
        返回球类型
        """
        return self.type

    def clear_image(self):
        """
        使用透明颜色填充图像
        """
        self.kill()  # 使用透明颜色填充图像

    def update(self):
        """
        更新球的方向
        """
        self.move_right()


class BallHandle(pygame.sprite.Sprite):
    def __init__(self):
        """
        初始化球处理类
        """
        super().__init__()
        self.ball_list = pygame.sprite.Group()

    def update(self, surface):
        """
        更新球的位置
        """
        for ball in self.ball_list:
            ball.draw(surface)
            ball.update()

    def reset(self):
        self.ball_list.empty()
