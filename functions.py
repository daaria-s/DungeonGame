from config import *
import pygame


def apply(coords):
    """Сдвигает координаты на высоту верхней панели"""
    return coords[0], coords[1] + PANEL_HEIGHT


def load_image(name):
    """Загружает изображение"""
    return pygame.image.load(name).convert_alpha()
