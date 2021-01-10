from dungeon import Dungeon
from interface import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Magic Dungeon')
    screen = pygame.display.set_mode(SIZE)

    dungeon = Dungeon()

    # EDIT
    # fix bug with new play music when you close settings panel
    windows = {
        'menu': Window('menu', [
            Image('menu/background', (0, 0)),
            Image('menu/title', (206, 10)),
            Button('menu/play', (192, 190), 'game', {'cycle': True}),
            Button('menu/load', (192, 290), 'load', {'cycle': True}),
            Button('menu/settings', (192, 390), 'settings', {'cycle': True}),
            Button('menu/exit', (192, 490), 'exit', {'cycle': True}),
            Image('menu/fire', (40, 277), {'speed': 6}),
            Image('menu/fire', (407, 277), {'speed': 6}),
        ],
                       importance=True),
        'settings': Window('settings', [
            AntiButton('settings/panel', (97, 152), 'menu'),
            Image('settings/music', (131, 212)),
            Image('settings/sounds', (131, 330)),
            Image('settings/scrollbar', (309, 233)),
            Image('settings/scrollbar', (309, 351)),
            Slider('settings/slider', (442, 225), (309, 442), 'set_music_volume'),
            Slider('settings/slider', (442, 343), (309, 442), 'set_sounds_volume'),
        ]
                           ),
        'load': Window('load', []),
        'exit': Window('exit', []),
        'game': Window('game', [dungeon], music_name='game', importance=True),
        'inventory': Window('inventory', [Inventory(dungeon.player)]),
        'save': Window('save', [])

    }

    current_window = windows['menu']
    clock = pygame.time.Clock()
    while True:
        current_window = windows[current_window.update(screen, pygame.event.get())]
        pygame.display.flip()
        clock.tick(FPS)
