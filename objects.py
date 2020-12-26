import pygame
from config import *
from animator import Animator


class Object:

    def __init__(self, path, position, name):
        self.position = position
        self.name = name
        self.animator = Animator('Sprites/' + path, True)

    def show(self):
        return self.animator.next_(), apply((self.position[0] * TILE, self.position[1] * TILE))


class Wall(Object):

    def __init__(self, position):
        super().__init__('wall', position, 'wall')


class Empty(Object):

    def __init__(self, position):
        super().__init__('ground', position, 'empty')


class Teleport(Object):

    def __init__(self, position, number):
        super().__init__('ground', position, 'teleport')
        self.number = number


class Box(Object):

    def __init__(self, position):
        super().__init__('ground', position, 'box')  # поставить правильный спрайт


class Chest(Object):

    def __init__(self, position):
        super().__init__('ground', position, 'chest')  # поставить правильный спрайт
