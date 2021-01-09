from animator import Animator
from functions import *


class Object:

    def __init__(self, path, position, name):
        self.position = position
        self.name = name
        self.animator = Animator('Sprites/' + path)

    def show(self, surf):
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


class Wall(Object):

    def __init__(self, position):
        super().__init__('wall', position, 'wall')


class Empty(Object):

    def __init__(self, position):
        super().__init__('ground', position, 'empty')


class Teleport(Object):

    def __init__(self, position, number):
        super().__init__('ground', position, 'teleport')
        self.number = number


class Box(Object):

    def __init__(self, position):
        super().__init__('box', position, 'box')

    def move(self, new_position, direction):
        self.position = new_position
        self.animator.start('move_' + direction)


class Chest(Object):

    def __init__(self, position, object, color=None):
        super().__init__('chest_02', position, 'chest')
        if object == 'key':
            self.inside = Key(self.position, color)
        elif object == 'potion':
            self.inside = Potion(self.position, 'green')
        self.stage = 0

    def touch(self):
        if self.stage == 0:
            self.animator.start('die')
            self.inside.animator.start('appearance')
            self.stage += 1
        elif self.stage == 1:
            self.inside.animator.start('die')
            self.stage += 1
            return self.inside.name
        else:
            return '__empty__'

    def show(self, surf):
        image, shift = self.inside.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


class Door(Object):

    def __init__(self, position, color):
        super().__init__('doors/' + color, position, 'door')
        self.color = color
        self.inside = None
        self.stage = 0

    def touch(self):
        if self.stage == 0:
            self.animator.start('die')
            self.stage += 1
        else:
            return '__empty__'

    def show(self, surf):
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))


class Key(Object):

    def __init__(self, position, color):
        super().__init__('keys/' + color, position, 'key')
        self.color = color
        self.name = color + '_key'


class Potion(Object):
    def __init__(self, position, color):
        super().__init__('keys/' + color, position, 'key')
        self.color = color
        self.name = 'health'


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
            music.play_sound('next_window')
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
            'red_key': (load_image('Sprites/inventory/red_key.png'), 'This key opens red doors'),

            'blue_key': (
                load_image('Sprites/inventory/blue_key.png'), 'This key opens blue doors'),

            'health': (
                load_image('Sprites/inventory/green_key.png'), 'This potion gives +1 health')
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
                    counter += 1
                else:
                    params = (None, '')
                self.slots[i].append(InventorySlot(
                    (100 + INVENTORY_INDENT + k * (INVENTORY_IMAGE_SIZE[0] + INVENTORY_INDENT),
                     100 + INVENTORY_INDENT + i * (INVENTORY_IMAGE_SIZE[1] + INVENTORY_INDENT)),
                    *params))

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


class TextBox(AnimatedElement):
    def __init__(self, name, position, function):
        super().__init__('Sprites/' + name, position)
        self.input_ = Text((position[0] + 15, position[1] + 15), DESCRIPTION_COLOR, text='')
        self.input_.font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 30)

    def show(self, surf):
        super().show(surf)
        self.input_.show(surf)


class InputBox(TextBox):
    def __init__(self, name, position, function):
        super().__init__(name, position, function)

    def key_down(self, key):
        if 48 <= key <= 57 or 97 <= key <= 122:
            if len(self.input_.text) < 14:
                self.input_.text += str(chr(key))
        elif key == 8:
            self.input_.text = self.input_.text[:-1]

    def show(self, surf):
        super().show(surf)
        self.input_.show(surf)
