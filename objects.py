from animator import Animator
from functions import *


class Object:

    def __init__(self, path, position, name):
        self.position = position
        self.name = name
        self.animator = Animator('Sprites/' + path, {'static': True})

    def show(self, surf):
        surf.blit(self.animator.next_()[0], apply((self.position[0] * TILE,
                                                   self.position[1] * TILE)))


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
        super().__init__('box', position, 'box')


class Chest(Object):

    def __init__(self, position):
        super().__init__('chest', position, 'chest')
