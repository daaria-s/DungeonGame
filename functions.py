from config import *
import pygame


def apply(coords):
    """Сдвигает координаты на высоту верхней панели"""
    return coords[0], coords[1] + PANEL_HEIGHT


def load_image(name):
    """Загружает изображение"""
    return pygame.image.load(name).convert_alpha()


def convert_coords(position):
    if position[0] in (0, 9):
        return abs(position[0] - 9), position[1]
    return position[0], abs(position[1] - 11)
