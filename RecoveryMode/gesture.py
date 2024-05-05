from settings import SCREEN_WIDTH
import pygame
import os


class Gesture(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/bar/scroll.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() // 1.2, self.image.get_height() // 1.3))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, self.rect.height // 2)
        self.gesture_images = []
        self.gesture_filenames = []  # 新增一个列表来存储文件名
        self.selected_index = 0  # 默认选中第一个图片，确保这一行在load_gesture_images之前
        self.load_gesture_images('Assets/gesture')
        self.prepare_gestures()

    def load_gesture_images(self, path):
        """加载所有手势图片并存储其文件名"""
        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)
            image = pygame.image.load(full_path).convert_alpha()
            self.gesture_images.append(image)
            self.gesture_filenames.append(filename)  # 存储文件名

    def prepare_gestures(self):
        """在bar上居中绘制手势图片，并铺满一行，不包含bar.png背景，同时缩小图片尺寸"""
        total_width = 0
        scaled_gesture_images = []
        for gesture_image in self.gesture_images:
            # 缩小图片尺寸到原来的80%
            scaled_width = int(gesture_image.get_width() * 0.3)
            scaled_height = int(gesture_image.get_height() * 0.3)
            scaled_image = pygame.transform.scale(gesture_image, (scaled_width, scaled_height))
            scaled_gesture_images.append(scaled_image)
            if total_width + scaled_width <= self.rect.width:
                total_width += scaled_width
            else:
                break

        start_x = (self.rect.width - total_width) // 2

        # 清空temp_surface
        temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))  # 使用完全透明的颜色填充

        x = start_x
        for index, gesture_image in enumerate(scaled_gesture_images):
            if x + gesture_image.get_width() > self.rect.width:
                break
            temp_surface.blit(gesture_image, (x, 0))
            if index == self.selected_index:
                pygame.draw.rect(temp_surface, (255, 0, 0),
                                 (x, 0, gesture_image.get_width(), gesture_image.get_height()), 5)
            x += gesture_image.get_width()

        self.image = temp_surface

    def select_gesture(self, index):
        """根据传入的索引值选中图片，并重新准备手势图片"""
        if 0 <= index < len(self.gesture_images) and index != self.selected_index:
            self.selected_index = index
            self.prepare_gestures()

    def get_selected_gesture_name(self):
        """获取当前被框选图片的文件名"""
        if self.gesture_filenames:
            # print(self.gesture_filenames[self.selected_index])
            return self.gesture_filenames[self.selected_index]
        return None

    def get_gesture_count(self):
        """返回铺在上面的图片的数量"""
        return len(self.gesture_images)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, surface, index):
        self.select_gesture(index)
        self.draw(surface)
        # 使用select_gesture来更新选中的图片
        # print(self.get_selected_gesture_name())
