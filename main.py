import pygame
import sys
from config import *
import config
from drawing import Drawing
from dungeon import Dungeon
from interface import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Magic Dungeon')
        self.screen = pygame.display.set_mode(SIZE)

        self.drawing = Drawing(self.screen)
        self.dungeon = Dungeon()

        self.windows = {
            'menu': (self.menu_update, self.menu_event_handler),
            'settings': (self.settings_update, self.settings_event_handler),
            'load': (self.load_update, self.load_event_handler),
            'exit': (lambda: sys.exit(1), None),
            'game': (self.game_update, self.game_event_handler),
            'inventory': (self.inventory_update, self.inventory_event_handler)
        }
        self.updater, self.event_handler = self.windows['menu']

        self.menu_objects = [
            Image('menu/background', (0, 0)),
            Image('menu/title', (192, 10)),
            Button('menu/buttons/play', (192, 100), 'game'),
            Button('menu/buttons/load', (192, 200), 'load'),
            Button('menu/buttons/settings', (192, 300), 'settings'),
            Button('menu/buttons/exit', (192, 400), 'exit'),
            Image('menu/fire', (40, 100)),
            Image('menu/fire', (390, 100))
        ]

        self.settings_objects = [
            Panel('settings/panel', (192, 100), 'menu'),
            Image('settings/music', (212, 170)),
            Image('settings/sounds', (212, 240)),
            Image('settings/scrollbar', (272, 170)),
            Image('settings/scrollbar', (272, 240)),
            Slider('settings/slider', (272, 170), (272, 372)),
            Slider('settings/slider', (272, 240), (272, 372))
            
        ]

        self.game_objects = [
            Image('game/panel/background', (0, 0)),
            Image('game/panel/action_points', (250, 10)),
            Text(self.dungeon.player, 'action_points', (290, 13), ACTION_POINTS_COLOR),
            Image('game/panel/damage', (170, 10)),
            Text(self.dungeon.player, 'damage', (210, 13), DAMAGE_COLOR),
            Button('game/panel/exit', (550, 10), 'menu'),
            Image('game/panel/health', (50, 10)),
            Text(self.dungeon.player, 'hit_points', (90, 13), HP_COLOR),
            Button('game/panel/inventory', (450, 10), 'inventory'),
            Button('game/panel/save', (500, 10), 'save')
        ]

        self.inventory_objects = [
            Panel('game/inventory', (192, 100), 'game')
        ]

    def menu_event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self.menu_objects:
                    target = obj.press(event.pos)
                    if target:
                        return target

        for obj in self.menu_objects:
            obj.move(pygame.mouse.get_pos())

        return 'menu'

    def menu_update(self):
        for obj in self.menu_objects:
            self.screen.blit(*obj.show())

    def settings_event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self.settings_objects:
                    target = obj.press(event.pos)
                    if target:
                        return target
            elif event.type == pygame.MOUSEBUTTONUP:
                for obj in self.settings_objects:
                    if isinstance(obj, Slider):
                        obj.unpress(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                for obj in self.settings_objects:
                    obj.move(event.pos)
        return 'settings'

    def settings_update(self):
        for obj in self.settings_objects:
            self.screen.blit(*obj.show())

    def load_event_handler(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 'menu'
        return 'load'

    def load_update(self):
        pass

    def game_event_handler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if config.TURN == 1:
                    self.dungeon.player_move(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self.game_objects:
                    target = obj.press(event.pos)
                    if target:
                        return target

        return 'game'

    def game_update(self):
        if config.TURN == 2:
            self.dungeon.enemies_move()

        for obj in self.game_objects:
            self.screen.blit(*obj.show())

        self.drawing.dungeon(self.dungeon)

    def inventory_update(self):
        pass

    def inventory_event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self.inventory_objects:
                    target = obj.press(event.pos)
                    if target:
                        return target
        return 'inventory'

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.updater, self.event_handler = self.windows[self.event_handler(pygame.event.get())]
            self.updater()
            pygame.display.flip()
            clock.tick(FPS)

    def exit(self):
        pygame.quit()
        sys.exit(1)


Game().run()
