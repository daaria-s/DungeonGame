from dungeon import Dungeon
from interface import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Magic Dungeon')
    screen = pygame.display.set_mode(SIZE)

    windows = {
        'menu': Window('menu', [Image('menu/background', (0, 0)),
                                Image('menu/title', (206, 10)),
                                Button('menu/play', (192, 190), 'game'),
                                Button('menu/load', (192, 290), 'load'),
                                Button('menu/settings', (192, 390), 'settings'),
                                Button('menu/exit', (192, 490), 'exit'),
                                Image('menu/fire', (40, 277)),
                                Image('menu/fire', (407, 277))]
                       ),
        'settings': Window('settings', [AntiButton('settings/panel', (97, 152), 'menu'),
                                        Image('settings/music', (131, 212)),
                                        Image('settings/sounds', (131, 330)),
                                        Image('settings/scrollbar', (309, 212)),
                                        Image('settings/scrollbar', (309, 330)),
                                        Slider('settings/slider', (309, 204), (309, 442)),
                                        Slider('settings/slider', (309, 322), (309, 442))]
                           ),
        'load': Window('load', []),
        'exit': Window('exit', []),
        'game': Window('game', [Dungeon()]),
        'inventory': Window('inventory', [AntiButton('game/inventory', (97, 97), 'game')]),
        'save': Window('save', [])

    }

    current_window = windows['menu']
    clock = pygame.time.Clock()
    while True:
        current_window = windows[current_window.update(screen, pygame.event.get())]
        pygame.display.flip()
        clock.tick(FPS)
