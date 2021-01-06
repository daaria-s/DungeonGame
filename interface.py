from animator import Animator
import pygame


class Element:

    def __init__(self, path, position, anim_cycle=False):
        self.animator = Animator(path, cycle=anim_cycle)
        self.position = position
        self.rect = self.animator.next_()[0].get_rect(topleft=position)

    def press(self, mouse_pos):
        pass

    def move(self, mouse_pos):
        pass

    def show(self):
        image, shift = self.animator.next_()
        return image, (self.position[0] + shift[0], self.position[1] + shift[1])


class Button(Element):

    def __init__(self, name, position, target):
        super().__init__('Sprites/' + name, position, anim_cycle=True)
        self.target = target

    def press(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return self.target

    def move(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.animator.animation == 'idle':
                self.animator.start('hover')
        else:
            self.animator.start('idle')


class Image(Element):

    def __init__(self, name, position):
        super().__init__('Sprites/' + name, position)


class Panel(Element):

    def __init__(self, name, position, target):
        super().__init__('Sprites/' + name, position)
        self.target = target

    def press(self, mouse_pos):
        if not self.rect.collidepoint(mouse_pos):
            return self.target


class Slider(Element):

    def __init__(self, name, position, borders):
        super().__init__('Sprites/' + name, position)
        self.capture = False
        self.borders = borders

    def press(self, mouse_pos):
        self.capture = self.rect.collidepoint(mouse_pos)

    def unpress(self, mouse_pos):
        self.capture = False

    def move(self, mouse_pos):
        if self.capture:
            if self.borders[0] <= mouse_pos[0] <= self.borders[1]:
                x = mouse_pos[0]
            elif mouse_pos[0] < self.borders[0]:
                x = self.borders[0]
            elif mouse_pos[0] > self.borders[1]:
                x = self.borders[1]
            self.position = (x, self.position[1])
            self.rect = self.animator.next_()[0].get_rect(topleft=self.position)


class Text:

    def __init__(self, target, attr_name, position, color):
        self.target = target
        self.attr_name = attr_name
        self.position = position
        self.color = color

        self.font = pygame.font.Font(None, 40)

    def show(self):
        return self.font.render(str(getattr(self.target, self.attr_name)), True, self.color), self.position

    def press(self, mouse_pos):
        pass
