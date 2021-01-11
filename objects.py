from animator import Animator
from functions import *


class Object:

    def __init__(self, path, position, name):
        self.position = position  # позиция
        self.name = name  # имя объекта
        self.animator = Animator('Sprites/' + path)  # аниматор

    def show(self, surf):
        """Отображение объекта"""
        image, shift = self.animator.next_()
        # получаем следущий кадр анимации и смещение
        # отображаем его на поверхность с учетом смещения
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


class Wall(Object):
    """Класс стены"""

    def __init__(self, position):
        super().__init__('wall', position, 'wall')


class Empty(Object):
    """Класс пустой клетки"""

    def __init__(self, position):
        super().__init__('ground', position, 'empty')


class Teleport(Object):
    """Класс телепорта"""

    def __init__(self, position, number):
        super().__init__('ground', position, 'teleport')
        self.number = number  # номер комнаты, в которую ведет этот телепорт


class Box(Object):
    """Класс коробки"""

    def __init__(self, position):
        super().__init__('box', position, 'box')

    def move(self, new_position, direction):
        """Движение в новую позицию"""
        self.position = new_position  # меняем позицию
        self.animator.start('move_' + direction)  # начинаем анимацию движения


class Chest(Object):

    def __init__(self, position, object_, color=None):
        super().__init__('chest', position, 'chest')
        if object_ == 'key':
            self.inside = Key(self.position, color)
        elif object_ == 'potion':
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

    def __init__(self, position, color):
        super().__init__('doors/' + color, position, 'door')
        self.color = color
        self.inside = None
        self.stage = 0

    def touch(self, has_key):
        if self.stage == 0:
            if has_key:
                self.animator.start('die')
                self.stage += 1
        else:
            return '__empty__'


class Key(Object):
    """Класс ключа"""

    def __init__(self, position, color):
        super().__init__('keys/' + color, position, color + '_key')
        self.color = color  # цвет ключа


class Potion(Object):
    def __init__(self, position, color):
        super().__init__('potions/' + color, position, 'health')
        self.color = color
