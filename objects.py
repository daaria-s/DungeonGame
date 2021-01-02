import pygame
import config
import os
import sys

buttons = pygame.sprite.Group()
background = pygame.sprite.Group()
settings = pygame.sprite.Group()


class Object:

    def __init__(self, image, position, name):
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            (config.TILE, config.TILE))
        self.position = position
        self.name = name

    def show(self):
        return self.image, config.apply((self.position[0] * config.TILE, self.position[1] * config.TILE))


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


def load_image(name, colorkey=None):
    fullname = os.path.join('Sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Mattone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        image = load_image('mattone.png', -1)
        super(Mattone, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x, self.y = x, y


class Button(pygame.sprite.Sprite):

    def __init__(self, image, x, y, image2=''):
        super().__init__(buttons)

        self.image1 = load_image(image)
        if image2:
            self.image2 = load_image(image2)

        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def pressed(self, x, y, function):
        if self.rect[0] <= x <= self.rect[2] + self.rect[0] and self.rect[1] <= y <= self.rect[3] + self.rect[1]:
            function()

    def motion(self, x, y):
        if self.rect[0] <= x <= self.rect[2] + self.rect[0] and self.rect[1] <= y <= self.rect[3] + self.rect[1]:
            self.image = self.image2
        else:
            self.image = self.image1


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self, background)  # call Sprite initializer
        self.image = load_image(image_file)
        self.rect = self.image.get_rect()


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self, settings)
        self.image = load_image(image, -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
