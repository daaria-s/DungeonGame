import os
from functions import *
from config import *


class Animator:

    def __init__(self, path, static=False, cycle=False):
        self.animations = {i: [load_image(path + '/' + i + '/' + k) for k in os.listdir(path + '/' + i)] for i in os.listdir(path)}
        self.animation = 'idle'
        self.counter = 0
        self.sub_counter = 0

        self.static = static
        self.cycle = cycle

        self.shift = (0, 0)

    def next_(self):
        if not self.static:
            self.sub_counter += 1
            if self.sub_counter == 2:
                self.counter += 1
                self.sub_counter = 0
            if self.counter >= len(self.animations[self.animation]):
                if self.animation == 'die':
                    self.counter -= 1
                else:
                    if self.cycle:
                        self.start(self.animation)
                    else:
                        self.start('idle')
        return self.animations[self.animation][self.counter], self.shift

    def start(self, name):
        self.animation = name
        if name == 'move_right':
            self.shift = (-TILE, 0)
        elif name == 'move_down':
            self.shift = (0, -TILE)
        elif name == 'attack_left':
            self.shift = (-TILE, 0)
        elif name == 'attack_up':
            self.shift = (0, -TILE)
        else:
            self.shift = (0, 0)
        self.counter = 0
        self.sub_counter = 0
