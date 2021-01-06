import pygame
import config
import os
import sys
from animator import Animator
from functions import *

buttons = pygame.sprite.Group()
background = pygame.sprite.Group()
settings = pygame.sprite.Group()
sliders = pygame.sprite.Group()


class Object:

    def __init__(self, path, position, name):
        self.position = position
        self.name = name
        self.animator = Animator('Sprites/' + path, True)

    def show(self):
        return self.animator.next_()[0], apply((self.position[0] * TILE,
                                                self.position[1] * TILE))


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
        super().__init__('Sprites/ground.png', position, 'chest')  # поставить правильный спрайт


def load_image(name, colorkey=None):
    # EDIT
    # Same function exist in functions.py
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
    def __init__(self, x, y, image, groups=None):
        pygame.sprite.Sprite.__init__(self, settings)
        self.image = load_image(image, -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, image, ):
        pygame.sprite.Sprite.__init__(self, sliders)
        self.image = load_image(image, -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.pressed = False

    def update(self, x, y, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.x < x < self.rect.x + 27 and self.rect.y < y < self.rect.y + 27:
            self.pressed = True
        elif event.type == pygame.MOUSEMOTION and self.pressed:
            if 190 < x < 350:
                self.rect.x = x
