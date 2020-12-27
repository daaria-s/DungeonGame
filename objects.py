import pygame
from animator import Animator
from functions import *


class Object:

    def __init__(self, path, position, name):
        self.position = position
        self.name = name
        self.animator = Animator('Sprites/' + path, True)

    def show(self):
        image, shift = self.animator.next_()
        return image, apply((self.position[0] * TILE + shift[0],
                             self.position[1] * TILE + shift[1]))


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
