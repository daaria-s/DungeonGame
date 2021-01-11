import pygame


class Music:
    """Класс музыки"""

    def __init__(self):
        pygame.init()
        self.sounds = {
            'hit': pygame.mixer.Sound('Sounds/tuk.mp3'),
            'button_down': pygame.mixer.Sound('Sounds/tuk.mp3'),
            'next_window':  pygame.mixer.Sound('Sounds/WindowChange.mp3'),
            'defeat': pygame.mixer.Sound('Sounds/Defeat.mp3'),
            'fail': pygame.mixer.Sound('Sounds/Fail.mp3')
        }
        self.musics = {
            'main': 'Sounds/menu_music1.mp3',
            'game': 'Sounds/game_music1.mp3',
            'defeat': 'Sounds/Defeat.mp3',

        }

    def play_sound(self, name):
        """Проиграть звук по имени"""
        self.sounds[name].play()

    def play_music(self, name):
        """Включить музыку по имени"""
        pygame.mixer.music.load(self.musics[name])
        pygame.mixer.music.play()

    def set_music_volume(self, volume):
        """Установить громкость музыки"""
        pygame.mixer.music.set_volume(volume)

    def set_sounds_volume(self, volume):
        """Установить громкость звуков"""
        for sound in self.sounds.values():
            sound.set_volume(volume)
