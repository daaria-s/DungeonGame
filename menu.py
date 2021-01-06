import pygame

from objects import Button, Background


class Menu:
    def __init__(self, surf):
        self.surf = surf

        Button('dungeon.png', 190, 20)
        self.backGround = Background('background.png')
        self.start = Button('button_play\\00.png', 210, 150, 'button_play\\01.png')
        self.load = Button('button_load\\00.png', 210, 250, 'button_load\\01.png')
        self.settings = Button('button_settings\\00.png', 210, 350, 'button_settings\\01.png')
        self.exit = Button('button_exit\\00.png', 210, 450, 'button_exit\\01.png')
        self.settings_open = False
