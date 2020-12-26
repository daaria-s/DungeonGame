import os
import pygame


class Animator:

    def __init__(self, path, static=False):
        self.animations = {i: [pygame.image.load(path + '/' + i + '/' + k).convert_alpha() for k in os.listdir(path + '/' + i)] for i in os.listdir(path)}
        self.animation = 'idle'
        self.counter = 0
        self.sub_counter = 0
        self.static = static

    def next_(self):
        if not self.static:
            self.sub_counter += 1
            if self.sub_counter == 4:
                self.counter += 1
                self.sub_counter = 0
            if self.counter >= len(self.animations[self.animation]):
                self.animation = 'idle'
                self.counter = 0
        return self.animations[self.animation][self.counter]

    def start(self, name):
        self.animation = name
        self.counter = 0
        self.sub_counter = 0
