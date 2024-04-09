import random
import image

from settings import *

'''
ENEMY_SIZES 敌人的尺寸 170 * 200
LANE_COORDINATE 暂时使用 三条道路的坐标
ANIMATION_SPEED 动画的速度
'''


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_speed = 1
        self.enemy_animation_index = 0
        self.state = True
        self.enemy_frames = [image.load(f"Assets/Enemy/{el}.png", size=ENEMY_SIZES) for el in range(1, 7)]
        self.image = self.enemy_frames[self.enemy_animation_index]
        self.enemy_row = random.randint(0, 2)
        self.rect = self.image.get_rect(topleft=LANE_COORDINATE[self.enemy_row])

    def cross_line(self):
        """
        用于判断敌人是否过线，过线则敌人消失，用于后期判断玩家是否失败
        :return:
        """
        if self.rect.x <= 300:
            self.state = False

    def animation_state(self):
        """
        更新动画帧
        :return:
        """
        self.enemy_animation_index += ANIMATION_SPEED
        if self.enemy_animation_index >= len(self.enemy_frames):
            self.enemy_animation_index = 0
        self.image = self.enemy_frames[int(self.enemy_animation_index)]

    def update(self):
        """
        更新敌人类
        :return:
        """
        self.cross_line()
        if self.state:
            self.animation_state()
            self.rect.x -= self.enemy_speed

    def draw(self, surface):
        """
        用于将敌人画在屏幕上
        :param surface: SCREEN
        :return:
        """
        surface.blit(self.image, self.rect)


class EnemyHandle(pygame.sprite.Sprite):
    # 用于总体控制敌人类
    def __init__(self):
        super().__init__()
        self.enemy_number = 0
        # 敌人总数
        self.enemy_appear_speed = 2000
        # 敌人出现的速度
        self.enemy_interval = random.randint(1000, self.enemy_appear_speed)
        # 敌人出现的时间间隔
        self.last_appear_time = pygame.time.get_ticks()
        # 敌人上次出现的时间
        self.enemy_list = pygame.sprite.Group()
        # 用于存储敌人列表
        self.enemy_total = random.randint(25, 30)
        # 随机数规定敌人的总数

    def remove_enemy(self, enemy):
        """
        用于删除敌人，过线或者被杀死
        :param enemy: 将要删除的敌人
        :return:
        """
        if not enemy.state:
            self.enemy_list.remove(enemy)

    def try_add_enemy(self):
        """
        用于判断是否可以在敌人组中添加敌人，如果敌人的总数和敌人出现的时间间隔在规定时间内则成功添加
        :return:
        """
        current_time = pygame.time.get_ticks()
        if self.enemy_number <= self.enemy_total and current_time - self.last_appear_time >= self.enemy_interval:
            self.last_appear_time = current_time
            self.add_enemy(Enemy())

    def add_enemy(self, enemy):
        """
        用于在敌人组中添加敌人，并做相关随机数的重新修改
        @:param enemy 将要添加的敌人对象
        :return:
        """
        # 防止敌人出现重合现象
        for enemy_item in self.enemy_list:
            if enemy_item.enemy_row == enemy.enemy_row:
                if enemy_item.rect.colliderect(enemy.rect):
                    enemy.rect = enemy_item.rect.x + 170
                    break
        self.enemy_number += 1
        self.enemy_list.add(enemy)
        self.enemy_interval = random.randint(1000, self.enemy_appear_speed)
        self.enemy_total = random.randint(25, 30)

    def update(self, surface):
        """
        更新并绘制敌人组，并判断是否移除敌人
        :param surface:
        :return:
        """
        self.try_add_enemy()
        self.enemy_list.update()
        self.enemy_list.draw(surface)
        for enemy in self.enemy_list:
            self.remove_enemy(enemy)
