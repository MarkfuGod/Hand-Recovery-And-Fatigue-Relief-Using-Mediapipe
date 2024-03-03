import pygame
import random
import image
from settings import *
from handgesture import Handgesture

class Bomb(Handgesture):
    def __init__(self):
        #size
        random_size_value = random.uniform(BOMB_SIZE_RANDOMIZE[0], BOMB_SIZE_RANDOMIZE[1])
        size = (int(BOMB_SIZES[0] * random_size_value), int(BOMB_SIZES[1] * random_size_value))
        # moving
        moving_direction, start_pos = self.define_spawn_pos(size)
        # sprite
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        self.images = [image.load(f"Assets/bomb/{nb}.png", size=size, flip=moving_direction=="right") for nb in range(1, 7)] # load the images
        self.current_frame = 0
        self.animation_timer = 0
        

    def kill(self, handgestures): # remove the handgesture from the list
        handgestures.remove(self)
        return -BOMB_PENALITY
