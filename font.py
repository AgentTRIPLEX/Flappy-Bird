import os
import pygame

def removeExtension(path):
    a = path.split('.')
    a.pop(-1)
    return ".".join(a)

fonts = {removeExtension(f): f"fonts\\{f}" for f in os.listdir('fonts')}

def get(name, size):
    return pygame.font.Font(fonts[name], size)