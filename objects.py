from animator import Animator
from functions import *


class Object:

    def __init__(self, path, position, name):
        self.position = position
        self.name = name
        self.animator = Animator('Sprites/' + path)

    def show(self, surf):
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


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

    def move(self, new_position, direction):
        self.position = new_position
        self.animator.start('move_' + direction)


class Chest(Object):

    def __init__(self, position, object):
        super().__init__('chest_02', position, 'chest')
        if object == 'key':
            self.inside = Key(self.position, 'red')
        else:
            self.inside = Potion(self.position, 'green')
        self.stage = 0

    def touch(self):
        if self.stage == 0:
            self.animator.start('die')
            self.inside.animator.start('appearance')
            self.stage += 1
        elif self.stage == 1:
            self.inside.animator.start('die')
            self.stage += 1
            return self.inside.name
        else:
            return '__empty__'

    def show(self, surf):
        image, shift = self.inside.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


class Door(Object):

    def __init__(self, position):
        super().__init__('doors', position, 'chest')
        self.inside = None
        self.stage = 0

    def touch(self):
        if self.stage == 0:
            self.animator.start('die')
            self.inside.animator.start('appearance')
            self.stage += 1
        elif self.stage == 1:
            self.inside.animator.start('die')
            self.stage += 1
            return self.inside.name
        else:
            return '__empty__'

    def show(self, surf):
        image, shift = self.inside.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


class Key(Object):

    def __init__(self, position, color):
        super().__init__('keys/' + color, position, 'key')
        self.color = color
        self.name = color + '_key'


class Potion(Object):
    def __init__(self, position, color):
        super().__init__('keys/' + color, position, 'key')
        self.color = color
        self.name = 'health'
