from animator import Animator
import pygame
import config
from config import *
import sys
from functions import *


all_sprites = pygame.sprite.Group()


class Window:
    """Класс окна"""

    def __init__(self, name, objects, music_name='main'):
        self.name = name
        self.objects = objects
        self.music_name = music_name
        self.important_windows = ['menu', 'game', 'exit']
        self.first_load = True

        self.fade_in_counter = 0
        self.fade_out_counter = 60
        self.fade_target = None

        self.fader = pygame.Surface(SIZE)
        self.fader.fill(BLACK)

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
                        if target in self.important_windows and self.name in self.important_windows:
                            self.fade_target = target
                            self.fade_out_counter = 0
                        else:
                            return target
            elif event.type == pygame.MOUSEBUTTONUP:
                for obj in self.objects:
                    obj.button_up(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                for obj in self.objects:
                    obj.mouse_motion(event.pos)

        self.first_load = False
        return self.name

    def fade(self, surf, value):
        self.fader.set_alpha(int(value * 4.25))
        surf.blit(self.fader, (0, 0))

    def update(self, surf, events):
        if self.name == 'exit':
            pygame.quit()
            sys.exit(1)
        if self.first_load:
            # EDIT
            # fix buttons hover at first load
            if self.name in self.important_windows:
                music.play_music(self.music_name)
                self.fade_in_counter = 60
            self.first_load = False

        for obj in self.objects:
            obj.show(surf)

        if self.fade_in_counter != 0:
            self.fade(surf, self.fade_in_counter)
            self.fade_in_counter -= 1
        elif self.fade_out_counter != 60:
            self.fade(surf, self.fade_out_counter)
            self.fade_out_counter += 1
            if self.fade_out_counter == 60:
                self.first_load = True
                return self.fade_target

        if self.fade_in_counter != 0 or self.fade_out_counter != 60:
            return self.name
        if config.LOSE_COUNTER > 0:
            config.LOSE_COUNTER -= 1
        if config.LOSE_COUNTER == 1:
            config.LOSE_COUNTER = 0
            self.objects[0].new()
            return 'lose'

        return self.get_event(events)


class Element:
    """Абстрактный класс элемента в окне"""

    def __init__(self):
        pass

    def button_down(self, mouse_pos):
        """Функция нажатия мыши"""
        pass

    def button_up(self, mouse_pos):
        """Функция отпускания мыши"""
        pass

    def mouse_motion(self, mouse_pos):
        """Функция движения мыши"""
        pass

    def key_down(self, button):
        """Функция нажатия на клавиатуру"""
        pass

    def show(self, surf):
        pass


class AnimatedElement(Element):
    """Класс анимированного элемента в окне"""

    def __init__(self, path, position, animator_options=None):
        super().__init__()
        self.animator = Animator(path, animator_options)  # создаем аниматор
        self.position = position  # позиция
        self.rect = self.animator.next_()[0].get_rect(topleft=position)  # определяем прямоугольник

    def show(self, surf):
        """Отображение на поверхности"""
        image, shift = self.animator.next_()
        surf.blit(image, (self.position[0] + shift[0], self.position[1] + shift[1]))


class Button(AnimatedElement):
    """Класс кнопки"""

    def __init__(self, name, position, target, animator_options=None):
        super().__init__('Sprites/' + name, position, animator_options)
        self.target = target  # имя окна, в которое мы перейдем, если нажмем на эту кнопку

    def button_down(self, mouse_pos):
        """Функция нажатия мыши"""
        if self.rect.collidepoint(mouse_pos):  # если нажали на кнопку
            music.play_sound('button_down')  # проигрываем звук нажатия
            return self.target  # возвращаем имя окна, в которое нужно перейти

    def mouse_motion(self, mouse_pos):
        """Функция движения мыши"""
        if self.rect.collidepoint(mouse_pos):  # если навели на кнопку
            if self.animator.animation == 'idle':
                self.animator.start('hover')  # включаем анимацию наведения
        else:
            self.animator.start('idle')  # иначе включаем анимацию покоя


class Image(AnimatedElement):
    """Класс изображения"""

    def __init__(self, name, position, animator_options=None):
        super().__init__('Sprites/' + name, position, animator_options)


class AntiButton(AnimatedElement):
    """Класс анти-кнопки"""

    def __init__(self, name, position, target):
        super().__init__('Sprites/' + name, position)
        self.target = target  # имя окна, в которое мы перейдем, если нажмем на вне этой кнопки

    def button_down(self, mouse_pos):
        """Функция нажатия мыши"""
        if not self.rect.collidepoint(mouse_pos):  # если нажали не на кнопку
            return self.target  # возвращаем имя окна, в которое нужно перейти


class Slider(AnimatedElement):
    """Класс слайдера"""

    def __init__(self, name, position, borders, function):
        super().__init__('Sprites/' + name, position)
        self.capture = False  # нажат ли на слайдер
        self.borders = borders  # границы слайдера
        self.function = function  # функция, вызываемая при изменении значения

    def button_down(self, mouse_pos):
        """Функция нажатия мыши"""
        # проверяем нажали ли на слайдер
        if self.rect.collidepoint(mouse_pos):
            self.capture = True
        else:
            self.capture = False

    def button_up(self, mouse_pos):
        """Функция отпускания мыши"""
        self.capture = False

    def mouse_motion(self, mouse_pos):
        """Функция движения мыши"""
        if self.capture:  # если слайдер зажат
            # то двигаем его, не выходя за границы
            if self.borders[0] <= mouse_pos[0] <= self.borders[1]:
                x = mouse_pos[0]
            elif mouse_pos[0] < self.borders[0]:
                x = self.borders[0]
            elif mouse_pos[0] > self.borders[1]:
                x = self.borders[1]
            self.position = (x, self.position[1])  # меняем позицию
            self.rect = self.animator.next_()[0].get_rect(topleft=self.position)  # и прямоугольник
            # вызываем функцию, привязанную к изменению значения слайдера
            getattr(music, self.function)((x - self.borders[0]) / (self.borders[1] - self.borders[0]))


class Text(Element):
    """Класс текста"""

    def __init__(self, position, color, target=None, attr_name=None, text=None):
        super().__init__()
        self.position = position  # позиция
        self.color = color  # цвет
        self.target = target  # либо объект класса игрок
        self.attr_name = attr_name  # и имя атрибута, которе нужно отображать
        self.text = text  # либо статичный текста

        self.font = pygame.font.Font(None, 40)  # шрифт

    def show(self, surf):
        """Отображение на поверхности"""
        if self.target and self.attr_name:  # если есть объект класса игрок и его атрибут
            value = getattr(self.target, self.attr_name)  # то отображаем его
            surf.blit(self.font.render(str(value[0]) + '/' + str(value[1]), True, self.color), self.position)
        elif self.text:  # если есть статичный текст, то отбражаем его
            surf.blit(self.font.render(str(self.text), True, self.color), self.position)
        else:  # иначе отображаем пустую строку
            surf.blit(self.font.render('', True, self.color), self.position)


class Panel(Element):
    """Класс панели"""

    def __init__(self, target, active, yShift):
        super().__init__()
        self.background = Image('game/panel/background', (0, yShift + 0))
        self.active = active
        self.target = target
        self.objects = [
            Image('game/panel/health', (50, yShift + 10)),
            Text((90, yShift + 13), HP_COLOR, self.target, 'hit_points'),
            Image('game/panel/damage', (170, yShift + 10)),
            Text((210, yShift + 13), DAMAGE_COLOR, self.target, 'damage'),
            Image('game/panel/action_points', (290, yShift + 10)),
            Text((330, yShift + 13), ACTION_POINTS_COLOR, self.target, 'action_points'),
        ]

    def show(self, surf):
        """Отображение на поверхности"""
        self.background.show(surf)
        if self.active:
            for obj in self.objects:
                obj.show(surf)

    def change_target(self, new_target):
        if new_target:
            self.target = new_target
            self.active = True
        else:
            self.active = False


class InventorySlot(Element):
    """Класс слота в инвентаре"""

    def __init__(self, position, image, description):
        super().__init__()
        self.position = position  # позиция
        self.base = load_image('Sprites/inventory/slot.png')  # пустой слот инвентаря
        self.image = image  # содержимое слота
        self.rect = self.base.get_rect(topleft=position)  # прямоугольник
        self.description = Text(DESCRIPTION_POSITION, DESCRIPTION_COLOR, text=description)  # описание

    def show(self, surf):
        """Отображение на поверхности"""
        surf.blit(self.base, self.position)  # отображаем пустой слот
        if self.image:  # если есть содержимое,
            surf.blit(self.image, self.position)  # то отображаем его

    def show_description(self, surf):
        """Отображение описания"""
        self.description.show(surf)

    def button_down(self, mouse_pos):
        """Функция нажатия мыши"""
        if self.rect.collidepoint(mouse_pos):  # нажали ли на слот
            return True


class Inventory(Element):
    """Класс инвентаря"""

    def __init__(self, target):
        super().__init__()
        self.base = AntiButton('game/inventory', (97, 97), 'game')  # изображения инвентаря

        # словарь вида {названия содержимого в инвентаре: [картинка, описание]}
        self.image_keys = {
            'red_key': (load_image('Sprites/inventory/red_key.png'), 'This key open red doors'),
            'health': (load_image('Sprites/inventory/green_key.png'), 'This key open red doors')
        }

        self.target = target  # в какое окно мы перейдем, при выходе из инвентаря
        self.slots = []  # слоты
        self.active_slot = None  # выбранный слот

    def update(self):
        """Обновление слотов"""
        self.slots = []  # опустошаем слоты
        counter = 0
        for i in range(4):
            self.slots.append([])
            for k in range(5):
                # определяем параметры для нового слота
                if counter < len(self.target.inventory):
                    # слот с содержимым согласно инвентарю игрока
                    params = self.image_keys[self.target.inventory[counter]]
                else:
                    params = (None, '')
                self.slots[i].append(InventorySlot((100 + INVENTORY_INDENT + k * (INVENTORY_IMAGE_SIZE[0] + INVENTORY_INDENT),
                                                    100 + INVENTORY_INDENT + i * (INVENTORY_IMAGE_SIZE[1] + INVENTORY_INDENT)),
                                                   *params))
                counter += 1

        self.active_slot = None

    def show(self, surf):
        """Отображение на поверхности"""
        self.update()  # обновляем слоты
        self.base.show(surf)  # показываем картинку инвентаря
        for i in range(len(self.slots)):
            for k in range(len(self.slots[i])):
                self.slots[i][k].show(surf)  # показываем слоты
        if self.active_slot:  # если есть выбранный слот, то
            self.active_slot.show_description(surf)  # показываем его описание

    def button_down(self, mouse_pos):
        """Функция нажатия мыши"""
        res = self.base.button_down(mouse_pos)  # если нажали вне инвентаря
        if res:
            return res  # то переходим в игру
        for i in range(len(self.slots)):
            for k in range(len(self.slots[i])):  # если нажали на слот
                if self.slots[i][k].button_down(mouse_pos):
                    self.active_slot = self.slots[i][k]  # то он становится активным
                    return
        self.active_slot = None  # опустошаем активный слот
