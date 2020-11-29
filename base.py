class Base:
    VEL = 5

    def __init__(self, img, y):
        self.img = img
        self.width = self.img.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = y

    def get_rect(self):
        return 0, self.y, self.img.get_width(), self.img.get_height()

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if (self.x1 + self.width) < 0:
            self.x1 = self.x2 + self.width

        if (self.x2 + self.width) < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

    def is_colliding(self, bird):
        x1, y1, w1, h1 = bird.get_rect()
        x2, y2, w2, h2 = self.get_rect()
        x_diff = x1 - x2
        y_diff = y1 - y2
        return x_diff > -w1 and x_diff < w2 and y_diff > -h1 and y_diff < h2