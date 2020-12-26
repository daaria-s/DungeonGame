from config import *
import pygame


def apply(coords):
    return coords[0], coords[1] + PANEL_HEIGHT


def load_image(name):
    return pygame.image.load(name).convert_alpha()
