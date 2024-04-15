import pygame

import image


class Ball(pygame.sprite.Sprite):
    def __init__(self, card_type):
        super().__init__()
        # 在游戏设置区域定义移动速度
        self.card_move_speed = 5
        self.card_fire = image.load("Assets/ball/fire.png")
        self.card_golden = image.load("Assets/ball/golden.png")
        self.card_ice = image.load("Assets/ball/ice.png")
        self.card_ground = image.load("Assets/ball/ground.png")
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
        # 绘制所有卡片
        # if self.type == "card_fire":
        surface.blit(self.image, self.rect)
        # if self.type == "card_golden":
        #     surface.blit(self.card_golden, (self.rect.x, self.rect.y + 233))  # 233为卡片间的垂直间距，可调整
        # if self.type == "card_ice":
        #     surface.blit(self.card_ice, (self.rect.x, self.rect.y + 466))  # 466为第三张卡片的垂直位置，可调整
        # if self.type == "card_ground":
        #     surface.blit(self.card_ground, (self.rect.x, self.rect.y + 466))  # 466为第三张卡片的垂直位置，可调整

    def move_right(self):
        # 增加卡片移动速度到当前位置
        self.rect.x += 8
        print("------------------------------")
        print(str(self.card_move_speed))
        print("移动" + str(self.rect.x))
        print("------------------------------")
        # 注意：这里我们只移动self.rect的x值，因为draw方法中的位置是基于self.rect.x计算的

    def get_card_type(self):
        return self.type

    def clear_image(self):
        # 假设image_to_clear是一个pygame.Surface对象
        self.kill()  # 使用透明颜色填充图像

    def update(self):
        self.move_right()


class BallHandle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ball_list = pygame.sprite.Group()

    def update(self, surface):
        for ball in self.ball_list:
            ball.draw(surface)
            ball.update()
