import pygame

class Bird:
    ANIMATION_TIME = 5
    MAX_ROTATION = 5
    ROT_VEL = 20
    started = False

    def __init__(self, assets, x, y):
        self.x = x
        self.y = y
        self.assets = assets
        self.ticks = 0
        self.sprite_index = 0
        self.tilt = 0
        self.vel = 0
        self.height = y
        self.jump_ticks = 0
        self.score = 0

    def get_rect(self):
        return self.x, self.y, self.assets[0].get_width(), self.assets[0].get_height()

    def get_sprite(self):
        if (self.ticks % self.ANIMATION_TIME) == 0:
            self.sprite_index += 1

            if self.sprite_index == len(self.assets):
                self.sprite_index = 0

        if self.tilt <= -80:
            self.sprite_index = 1

        sprite = self.assets[self.sprite_index]
        return sprite

    def jump(self):
        Bird.started = True
        self.vel = -9.0
        self.jump_ticks = 0
        self.height = self.y

    def move(self, fps):
        if self.started:
            self.ticks += 1
            self.jump_ticks += 1

            d = (self.vel * self.jump_ticks) + (0.5 * (fps / 10) * (self.jump_ticks ** 2))

            if d >= 16:
                d = (d / abs(d)) * 16

            if d < 0:
                d -= 2

            self.y += d

            _, _, _, h = self.get_rect()
            if (d < 0) or (self.y < (self.height + h)):
                if self.tilt < self.MAX_ROTATION:
                    self.tilt = self.MAX_ROTATION

            else:
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL

    def draw(self, win):
        sprite = self.get_sprite()
        rotated_img = pygame.transform.rotate(sprite, self.tilt)
        new_rect = rotated_img.get_rect(center=sprite.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.get_sprite())
