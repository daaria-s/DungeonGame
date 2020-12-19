import pygame
import config


class Object:

    def __init__(self, image, position, name):
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            (config.TILE, config.TILE))
        self.position = position
        self.name = name

    def show(self):
        pass


class Wall(Object):

    def __init__(self, position):
        super().__init__('Sprites/wall.png', position, 'wall')


class Empty(Object):

    def __init__(self, position):
        super().__init__('Sprites/ground.png', position, 'empty')


class Teleport(Object):

    def __init__(self, position, number):
        super().__init__('Sprites/ground.png', position, 'teleport')
        self.number = number


class Box(Object):

    def __init__(self, position):
        super().__init__('Sprites/ground.png', position, 'box')  # поставить правильный спрайт


class Chest(Object):

    def __init__(self, position):
        super().__init__('Sprites/ground.png', position, 'chest')  # поставить правильный спрайт
