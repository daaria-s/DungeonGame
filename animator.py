import os
from functions import *
from config import *
import config


class Animator:
    """Класс-аниматор"""

    def __init__(self, path, options=None):
        # создаем словарь вида {имя анимации: [список из pygame.Surface]}
        self.animations = {i: [load_image(path + '/' + i + '/' + k)
                               for k in os.listdir(path + '/' + i)] for i in os.listdir(path)}
        self.animation = 'idle'  # по умолчанию стоит анимация покоя
        self.counter = 0  # текущий кадр анимации
        self.sub_counter = 0  # сколько тактов будет отображаться каждй кадр

        self.static = options.get('static', False) if options else False  # статичность картинки
        self.max_sub_counter = options.get('speed', 2) if options else 2  # задержка между кадрами анимации
        self.cycle = options.get('cycle', False) if options else False  # цикличность анимации

        self.shift = (0, 0)  # смещение спрайта при некоторых анимации

    def next_(self):
        """Следущий кадр анимации"""
        if not self.static:
            self.sub_counter += 1
            if self.sub_counter == self.max_sub_counter:  # делаем задержку между кадрами анимации
                self.counter += 1
                self.sub_counter = 0
            if self.counter >= len(self.animations[self.animation]):  # если закончили проигрывать текущую анимацию
                if self.animation == 'die':  # чтобы после анимации смерти не включалась анимация покоя
                    self.counter -= 1
                else:
                    if self.cycle:  # если анимация циклическая, то заново её запускаем
                        self.start(self.animation)
                    else:
                        self.start('idle')
        return self.animations[self.animation][self.counter], self.shift  # возвращаем кадр и смещение

    def start(self, name):
        """Начать новую анимацию"""
        self.animation = name  # меняем имя анимации

        # для некоторых анимаций необходимо смещение спрайта, чтобы они корректно отображались
        if name == 'move_right':
            self.shift = (-TILE, 0)
        elif name == 'move_down':
            self.shift = (0, -TILE)
        elif name == 'attack_left':
            self.shift = (-TILE, 0)
        elif name == 'attack_up':
            self.shift = (0, -TILE)
        else:
            self.shift = (0, 0)
        self.counter = 0  # обнуляем счетчик кадров
        self.sub_counter = 0  # обнуляем задержку
