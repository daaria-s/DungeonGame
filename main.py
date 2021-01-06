import pygame
from config import *
import config
from drawing import Drawing
from dungeon import Dungeon
from music import Music
from menu import Menu
import sys
from objects import buttons, settings, sliders, Slider


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Magic Dungeon')
        self.screen = pygame.display.set_mode(SIZE)

        self.drawing = Drawing(self.screen)
        self.dungeon = Dungeon()
        self.music = Music()
        self.menu = Menu(self.screen)

        self.first_slider = Slider(345, 61, 'settings/slider.png')
        self.second_slider = Slider(345, 151, 'settings/slider.png')

    def exit(self):
        sys.exit()

    def run_menu(self):
        self.music.menu_music()
        running = True

        self.drawing.menu(self.screen)
        while running:
            for event in pygame.event.get():
                self.music.update(event)
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    self.menu.start.motion(*pygame.mouse.get_pos())
                    self.menu.load.motion(*pygame.mouse.get_pos())
                    self.menu.settings.motion(*pygame.mouse.get_pos())
                    self.menu.exit.motion(*pygame.mouse.get_pos())
                    buttons.draw(self.screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.menu.start.pressed(*pygame.mouse.get_pos(), self.run_game)
                    self.menu.load.pressed(*pygame.mouse.get_pos(), self.choose_game)
                    self.menu.exit.pressed(*pygame.mouse.get_pos(), self.exit)
                    self.menu.settings.pressed(*pygame.mouse.get_pos(), self.show_settings)

            pygame.display.flip()


    def show_settings(self):
        self.menu.settings_open = True
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                x_pos, y_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_focused() and not (90 < x_pos < 496 and 140 < y_pos < 436):
                        self.drawing.menu(self.screen)
                        return
                sliders.update(x_pos - 90, y_pos - 140, event)
                self.music.settings(self.first_slider.rect.x, self.second_slider.rect.x)
            self.drawing.settings(self.screen)
            pygame.display.flip()
            clock.tick(100)

    def choose_game(self):
        print('load')

    def run_game(self):
        self.music.game_music()
        self.screen.fill((42, 42, 42))
        self.drawing.dungeon(self.dungeon)
        self.drawing.bottom_panel(self.dungeon, (0, 0))
        clock = pygame.time.Clock()
        running = True
        in_inventory = False
        while running:
            if not config.LOSE:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit()
                if event.type == pygame.KEYDOWN:
                    if config.TURN == 1 and not in_inventory:
                        self.dungeon.player_move(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not in_inventory:
                        self.drawing.bottom_panel(self.dungeon, event.pos)

                        # top panel buttons pressed
                        if 10 <= event.pos[1] <= 10 + PANEL_IMAGE_SIZE[1]:
                            if 450 <= event.pos[0] <= 450 + PANEL_IMAGE_SIZE[0]:  # inventory
                                self.drawing.inventory(self.dungeon)
                                in_inventory = True
                            if 500 <= event.pos[0] <= 500 + PANEL_IMAGE_SIZE[0]:  # save
                                print('SAVE')
                            if 550 <= event.pos[0] <= 550 + PANEL_IMAGE_SIZE[0]:  # exit
                                sys.exit(1)
                    elif event.button == 1 and in_inventory:
                        if event.pos[0] < 100 or event.pos[0] > 500 or event.pos[1] < 100 or event.pos[1] > 500:
                            in_inventory = False
                            self.screen.fill(BLACK)
                            self.drawing.dungeon(self.dungeon)
                            self.drawing.bottom_panel(self.dungeon, (0, 0))
                if in_inventory:
                    pass
                else:
                    if config.TURN == 2:
                        self.dungeon.enemies_move()

                self.drawing.top_panel(self.dungeon)
                self.drawing.dungeon(self.dungeon)
                clock.tick(FPS)


Game().run_menu()
