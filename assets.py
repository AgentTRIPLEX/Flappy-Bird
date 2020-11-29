import os
import pygame

def removeExtension(path):
    a = path.split('.')
    a.pop(-1)
    return ".".join(a)

assets = {}

for filename in os.listdir("assets"):
        path = f"assets\\{filename}"

        if os.path.isfile(path):
            assets[removeExtension(filename)] = pygame.image.load(path)

assets["bird"] = []
for filename in os.listdir("assets\\bird"):
    path = f"assets\\bird\\{filename}"
    assets["bird"].append(pygame.image.load(path))