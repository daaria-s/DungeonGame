from dungeon import Dungeon
from interface import *
from objects import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Magic Dungeon')
    screen = pygame.display.set_mode(SIZE)

    dungeon = Dungeon()

    # Создаем словарь вида {имя окна: класс окна}
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
        ]),
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
        'load': Window('load', [
            AntiButton('load/panel', (97, 152), 'menu'),
            Image('load/title', (211, 172)),
            TextBox('load/cell', (119, 263), ''),
            Button('load/load', (139, 350), 'game', {'cycle': True}),
            Button('load/cancel', (319, 350), 'menu', {'cycle': True}),
        ]),
        'exit': Window('exit', []),
        'game': Window('game', [dungeon], music_name='game'),
        'lose': Window('lose', [
            Image('lose/background', (0, 0)),
            Image('lose/lose_text', (196, 200)),
            Button('lose/menu', (104, 300), 'menu', {'cycle': True}),
            Button('lose/new_game', (352, 300), 'game', {'cycle': True}),
        ], music_name='defeat'),
        'inventory': Window('inventory', [Inventory(dungeon.player)],
                            music_name='game'),
        'save': Window('save', [
            AntiButton('save/panel', (97, 152), 'game'),
            Image('save/title', (211, 172)),
            InputBox('save/input_box', (119, 243), ''),
            Button('save/save', (119, 330), 'game', {'cycle': True}),
            Button('save/cancel', (319, 330), 'game', {'cycle': True}),
        ], music_name='game')

    }

    current_window = windows['menu']  # устанавливает текущее окно
    clock = pygame.time.Clock()
    while True:  # бесконечный игровой цикл
        # обновляем окно и делаем отрисовку в зависимости от произошедших событий
        current_window = windows[current_window.update(screen, pygame.event.get())]
        pygame.display.flip()  # обновление экрана
        clock.tick(FPS)  # задержка
