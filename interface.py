from animator import Animator
import pygame
from config import *
import sys
from config import music


class Window:

    def __init__(self, name, objects, music_name='main', run_music=False):
        self.name = name
        self.objects = objects
        self.music_name = music_name
        self.run_music = run_music
        self.first_load = True

    def update(self, surf, events):
        if self.first_load:
            if self.run_music:
                music.play_music(self.music_name)
            self.first_load = False

        self.first_load = True
        if self.name == 'exit':
            pygame.quit()
            sys.exit()
        for event in events:
            if event.type == pygame.QUIT:
                return 'exit'
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

        for obj in self.objects:
            obj.show(surf)
        self.first_load = False
        return self.name


class Element:

    def __init__(self):
        pass

    def button_down(self, mouse_pos):
        pass

    def button_up(self, mouse_pos):
        pass

    def mouse_motion(self, mouse_pos):
        pass

    def key_down(self, button):
        pass

    def show(self, surf):
        pass


class AnimatedElement(Element):

    def __init__(self, path, position, animator_options=None):
        super().__init__()
        self.animator = Animator(path, animator_options)
        self.position = position
        self.rect = self.animator.next_()[0].get_rect(topleft=position)

    def show(self, surf):
        image, shift = self.animator.next_()
        surf.blit(image, (self.position[0] + shift[0], self.position[1] + shift[1]))


class Button(AnimatedElement):

    def __init__(self, name, position, target, animator_options=None):
        super().__init__('Sprites/' + name, position, animator_options)
        self.target = target

    def button_down(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            music.play_sound('button_down')
            return self.target

    def mouse_motion(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.animator.animation == 'idle':
                self.animator.start('hover')
        else:
            self.animator.start('idle')


class Image(AnimatedElement):

    def __init__(self, name, position, animator_options=None):
        super().__init__('Sprites/' + name, position, animator_options)


class AntiButton(AnimatedElement):

    def __init__(self, name, position, target):
        super().__init__('Sprites/' + name, position)
        self.target = target

    def button_down(self, mouse_pos):
        if not self.rect.collidepoint(mouse_pos):
            return self.target


class Slider(AnimatedElement):

    def __init__(self, name, position, borders, function):
        super().__init__('Sprites/' + name, position)
        self.capture = False
        self.borders = borders
        self.function = function

    def button_down(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.capture = True
        else:
            self.capture = False

    def button_up(self, mouse_pos):
        self.capture = False

    def mouse_motion(self, mouse_pos):
        if self.capture:
            if self.borders[0] <= mouse_pos[0] <= self.borders[1]:
                x = mouse_pos[0]
            elif mouse_pos[0] < self.borders[0]:
                x = self.borders[0]
            elif mouse_pos[0] > self.borders[1]:
                x = self.borders[1]
            self.position = (x, self.position[1])
            self.rect = self.animator.next_()[0].get_rect(topleft=self.position)
            getattr(music, self.function)((x - self.borders[0]) / (self.borders[1] - self.borders[0]))


class Text(Element):

    def __init__(self, target, attr_name, position, color):
        super().__init__()
        self.target = target
        self.attr_name = attr_name
        self.position = position
        self.color = color

        self.font = pygame.font.Font(None, 40)

    def show(self, surf):
        value = getattr(self.target, self.attr_name)
        surf.blit(self.font.render(str(value[0]) + '/' + str(value[1]), True, self.color), self.position)


class Panel(Element):

    def __init__(self, target, active, yShift):
        super().__init__()
        self.background = Image('game/panel/background', (0, yShift + 0))
        self.active = active
        self.target = target
        self.objects = [
            Image('game/panel/health', (50, yShift + 10)),
            Text(self.target, 'hit_points', (90, yShift + 13), HP_COLOR),
            Image('game/panel/damage', (170, yShift + 10)),
            Text(self.target, 'damage', (210, yShift + 13), DAMAGE_COLOR),
            Image('game/panel/action_points', (290, yShift + 10)),
            Text(self.target, 'action_points', (330, yShift + 13), ACTION_POINTS_COLOR),
        ]

    def show(self, surf):
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
