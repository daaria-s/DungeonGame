from animator import Animator
import pygame
from config import *
import sys
from config import music
from functions import *

all_sprites = pygame.sprite.Group()


class Window:

    def __init__(self, name, objects, music_name='main', run_music=False):
        self.name = name
        self.objects = objects
        self.music_name = music_name
        self.run_music = run_music

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

        for obj in self.objects:
            obj.show(surf)

        if self.run_music and self.music_name != music.now_play:
            music.play_music(self.music_name)

        return self.get_event(events)


class Element(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
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
            getattr(music, self.function)(
                (x - self.borders[0]) / (self.borders[1] - self.borders[0]))


class Text(Element):

    def __init__(self, position, color, target=None, attr_name=None, text=None):
        super().__init__()
        self.position = position
        self.color = color
        self.target = target
        self.attr_name = attr_name
        self.text = text

        self.font = pygame.font.Font(None, 40)

    def show(self, surf):
        if self.target and self.attr_name:
            value = getattr(self.target, self.attr_name)
            surf.blit(self.font.render(str(value[0]) + '/' + str(value[1]), True, self.color),
                      self.position)
        elif self.text:
            surf.blit(self.font.render(str(self.text), True, self.color), self.position)
        else:
            surf.blit(self.font.render('', True, self.color), self.position)


class Panel(Element):

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

    def __init__(self, position, image, description):
        super().__init__()
        self.position = position
        self.base = load_image('Sprites/inventory/slot.png')
        self.image = image
        self.rect = self.base.get_rect(topleft=position)
        self.description = Text(DESCRIPTION_POSITION, DESCRIPTION_COLOR, text=description)

    def show(self, surf):
        surf.blit(self.base, self.position)
        if self.image:
            surf.blit(self.image, self.position)

    def show_description(self, surf):
        self.description.show(surf)

    def button_down(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True


class Inventory(Element):

    def __init__(self, target):
        super().__init__()
        self.base = AntiButton('game/inventory', (97, 97), 'game')

        self.image_keys = {
            'red_key': (load_image('Sprites/inventory/red_key.png'), 'This key open red doors'),

            'health': (load_image('Sprites/inventory/green_key.png'), 'This key open red doors')
        }

        self.target = target
        self.slots = []
        self.active_slot = None

    def update(self):
        self.slots = []
        counter = 0
        for i in range(4):
            self.slots.append([])
            for k in range(5):
                if counter < len(self.target.inventory):
                    params = self.image_keys[self.target.inventory[counter]]
                else:
                    params = (None, '')
                self.slots[i].append(InventorySlot(
                    (100 + INVENTORY_INDENT + k * (INVENTORY_IMAGE_SIZE[0] + INVENTORY_INDENT),
                     100 + INVENTORY_INDENT + i * (INVENTORY_IMAGE_SIZE[1] + INVENTORY_INDENT)),
                    *params))
                counter += 1

        self.active_slot = None

    def show(self, surf):
        self.update()
        self.base.show(surf)
        for i in range(len(self.slots)):
            for k in range(len(self.slots[i])):
                self.slots[i][k].show(surf)
        if self.active_slot:
            self.active_slot.show_description(surf)

    def button_down(self, mouse_pos):
        res = self.base.button_down(mouse_pos)
        if res:
            return res
        for i in range(len(self.slots)):
            for k in range(len(self.slots[i])):
                if self.slots[i][k].button_down(mouse_pos):
                    self.active_slot = self.slots[i][k]
                    return
        self.active_slot = None
