import pygame


# EDIT
# edit sounds and music files
class Music:
    """Класс музыки"""

    def __init__(self):
        pygame.init()
        self.sounds = {
            'hit': pygame.mixer.Sound('Sounds/tuk.mp3'),
            'button_down': pygame.mixer.Sound('Sounds/tuk.mp3'),
        }
        self.musics = {
            'main': 'Sounds/menu_music.mp3',
            'game': 'Sounds/melody.mp3',
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
