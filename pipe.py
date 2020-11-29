import pygame
import random

class Pipe:
    VEL = 5

    def __init__(self, img, x, gap=100):
        self.gap = gap
        self.x = x
        self.top_img = pygame.transform.flip(img, False, True)
        self.bottom_img = img
        self.height = random.randint(25, 225)
        self.top = self.height - self.top_img.get_height()
        self.bottom = self.height + self.gap
        self.passed = []
        self.added_pipe = False

    def get_width(self):
        return self.bottom_img.get_width()

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.top_img, (self.x, self.top))
        win.blit(self.bottom_img, (self.x, self.bottom))

    def is_colliding(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_img)

        bottom_mask = pygame.mask.from_surface(self.bottom_img)
        top_offset = (self.x - bird.x), (self.top - round(bird.y))
        bottom_offset = (self.x - bird.x), (self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return t_point or b_point