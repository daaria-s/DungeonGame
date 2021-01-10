from animator import Animator
from functions import *


class Object:
    """Класс объекта на игровом поле"""

    def __init__(self, path, position, name):
        self.position = position  # позиция
        self.name = name  # имя объекта
        self.animator = Animator('Sprites/' + path)  # аниматор

    def show(self, surf):
        """Отображение объекта"""
        image, shift = self.animator.next_()   # получаем следущий кадр анимации и смещение
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
    """Класс сундука"""

    def __init__(self, position):
        super().__init__('chest', position, 'chest')
        self.key = Key(self.position, 'red')  # содержимое сундука
        self.stage = 0  # стадия сундука

    def touch(self):
        """Функция удара по сундуку"""
        if self.stage == 0:  # если сундук закрыт
            self.animator.start('die')  # скрываем сундук
            self.key.animator.start('appearance')  # показываем содержимое
            self.stage += 1  # переходим к следущей стадии
        elif self.stage == 1:  # если сундук открыт, но ключ не забран
            self.key.animator.start('die')  # скрываем ключ
            self.stage += 1  # переходим к следущей стадии
            return self.key.color + '_key'  # возвращаем цвет ключа (нудно для помещения в инвентарь)
        else:  # если сундук открыт и ключ забран
            return '__empty__'

    def show(self, surf):
        """Отображение объекта"""
        # отображаем вначале содержимое сундука
        image, shift = self.key.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))
        # а потом сам сундук
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


class Key(Object):
    """Класс ключа"""

    def __init__(self, position, color):
        super().__init__('keys/' + color, position, 'key')
        self.color = color  # цвет ключа
