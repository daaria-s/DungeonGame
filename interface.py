import sys
from dungeon import Dungeon
from objects import *

all_sprites = pygame.sprite.Group()


class Window:

    def __init__(self, name, objects, music_name='main', run_music=False):
        self.name = name
        self.objects = objects
        self.music_name = music_name
        self.run_music = run_music
        self.first_open = True

    def get_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for obj in self.objects:
                    obj.key_down(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self.objects:
                    target = obj.button_down(event.pos)
                    if target:
                        return target
            elif event.type == pygame.MOUSEBUTTONUP:
                for obj in self.objects:
                    obj.button_up(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                for obj in self.objects:
                    obj.mouse_motion(event.pos)

        return self.name

    def update(self, surf, events):

        if self.run_music and self.music_name != music.now_play:
            if self.name == 'game':
                self.objects = [Dungeon()]
            music.play_music(self.music_name)

        for obj in self.objects:
            obj.show(surf)

        return self.get_event(events)

