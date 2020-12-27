import pygame
from config import *
import config
from drawing import Drawing
from dungeon import Dungeon
from music import Music
from menu import Menu
import sys
from objects import buttons


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Magic Dungeon')
        self.screen = pygame.display.set_mode(SIZE)

        self.drawing = Drawing(self.screen)
        self.dungeon = Dungeon()
        self.music = Music()
        self.menu = Menu(self.screen)

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
        running = True
        self.menu.settings_open = True
        self.drawing.settings(self.screen)

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    self.drawing.menu(self.screen)
            pygame.display.flip()

    def choose_game(self):
        print('load')

    def run_game(self):
        self.music.game_music()
        self.screen.fill((42, 42, 42))
        self.drawing.dungeon(self.dungeon)
        self.drawing.bottom_panel(self.dungeon, (0, 0))
        clock = pygame.time.Clock()
        running = True
        while running:
            if not config.LOSE:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # running = False
                        # self.music.menu_music()
                        self.exit()
                    if event.type == pygame.KEYDOWN:
                        if config.TURN == 1:
                            self.dungeon.player_move(event.key)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.drawing.bottom_panel(self.dungeon, event.pos)

                if config.TURN == 2:
                    self.dungeon.enemies_move()

                self.drawing.top_panel(self.dungeon)
                self.drawing.entities(self.dungeon)
                self.drawing.fps(clock)

                pygame.display.flip()
                clock.tick(FPS)

    pygame.quit()


Game().run_menu()
