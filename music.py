import pygame as pg


class Music:
    def __init__(self):
        pg.init()

        pg.mixer.music.load('Sounds/menu_music.mp3')
        pg.mixer.music.play()
        self.game_sound = pg.mixer.Sound('Sounds/tuk.mp3')
        self.sound2 = None
        self.sound3 = None

    def update(self, event):
            if event.type == pg.KEYUP:
                if event.key == pg.K_1:
                    pg.mixer.music.pause()
                elif event.key == pg.K_2:
                    pg.mixer.music.unpause()
                    pg.mixer.music.set_volume(0.5)
                elif event.key == pg.K_3:
                    pg.mixer.music.unpause()
                    pg.mixer.music.set_volume(1)
            pg.time.delay(20)

    def game_music(self):
        pg.mixer.music.load('Sounds/melody.mp3')
        pg.mixer.music.play()

    def menu_music(self):
        pg.mixer.music.play()
