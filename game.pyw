import pygame
import threading
import time
import os
import neat

import font
import messagebox
import settings

from assets import assets
from base import Base
from pipe import Pipe
from bird import Bird

pygame.init()

class Game:
    def __init__(self):
        self.WIDTH = assets["bg"].get_width()
        self.HEIGHT = assets["bg"].get_height()

        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()
        self.FPS = 20
        self.gen = 0

        y = assets["bg"].get_height() - assets["base"].get_height()
        self.base = Base(assets["base"], y)

        x = assets["bg"].get_width() // 4
        y = assets["bg"].get_height() // 2
        self.bird_args = assets["bird"], x, y

        self.reset()

    def mainloop(self, genomes=None, config=None):
        if settings.AI:
            self.gen += 1
            self.reset(True)

            self.nets = []
            self.ge = []

            for _, g in genomes:
                net = neat.nn.FeedForwardNetwork.create(g, config)
                self.nets.append(net)
                self.birds.append(Bird(*self.bird_args))
                g.fitness = 0
                self.ge.append(g)

        self.run = True
        add_pipe = True

        while self.run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                    if settings.AI:
                        pygame.quit()
                        quit()

            for pipe in self.pipes[:]:
                pipe.move()

                if (pipe.x + pipe.top_img.get_width()) < 0:
                    self.pipes.remove(pipe)

                if ((pipe.x + pipe.top_img.get_width() - 120) < 0) and not pipe.added_pipe:
                    add_pipe = True
                    pipe.added_pipe = True

                for bird in self.birds:
                    if (bird not in pipe.passed) and (pipe.x < bird.x):
                        bird.score += 1

                        if settings.AI:
                            self.ge[self.birds.index(bird)].fitness += 5

                        pipe.passed.append(bird)

            self.draw()

            for i, bird in enumerate(self.birds):
                bird.move()

                if settings.AI:
                    self.ge[i].fitness += 0.1

            self.handle_keys(pygame.key.get_pressed())

            self.base.move()

            threading.Thread(target=self.handle_collision).start()

            if add_pipe:
                if (not settings.AI and self.birds[0].started) or settings.AI:
                    self.add_pipe(self.WIDTH - 10)
                    add_pipe = False

        if not settings.AI:
            if messagebox.askyesno("Restart?", "Would You Like To Play Again?"):
                self.reset()
                return self.start()
            else:
                pygame.quit()

    def draw(self):
        self.win.blit(assets["bg"], (0,0))

        for pipe in self.pipes:
            while 1:
                try:
                    pipe.draw(self.win)
                    break
                except:
                    pass

        self.base.draw(self.win)

        for bird in self.birds:
            bird.draw(self.win)

        if len(self.birds) > 0:
            score = self.birds[0].score
        else:
            score = 0

        f = font.get('cpgb', 20)
        text = f.render(f"Score: {score}", True, (255, 255, 255))
        self.win.blit(text, ((self.WIDTH - 10 - text.get_width()), 10))

        if settings.AI:
            birds = len(self.birds)
            text = f.render(f"Gen: {self.gen} ({birds})", True, (255, 255, 255))
            self.win.blit(text, (0, 10))

        pygame.display.update()

    def start(self):
        if not settings.AI:
            return self.mainloop()

        filename = "neat-config.txt"
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, filename)

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)

        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())

        winner = p.run(self.mainloop, 50)

        print([winner])

        pygame.quit()

    def add_pipe(self, x):
        p = Pipe(assets["pipe"], x, 110)
        self.pipes.append(p)

    def handle_keys(self, keys):
        pipe_ind = 0
        if settings.AI:
            if len(self.birds) > 0:
                if len(self.pipes) > 1:
                    if self.birds[0].x > (self.pipes[0].x + self.pipes[0].top_img.get_width()):
                        pipe_ind = 1

            for i, bird in enumerate(self.birds):
                if len(self.pipes) > 0:
                    pipe = self.pipes[pipe_ind]
                    output = self.nets[i].activate((bird.y, abs(bird.y - pipe.height), abs(bird.y - pipe.bottom)))

                    if output[0] > 0.5:
                        bird.jump()

        else:
            if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
                self.birds[0].jump()
                time.sleep(0.3)

    def handle_collision(self):
        for i, bird in enumerate(self.birds):
            if self.base.is_colliding(bird):
                self.over(bird)

            for pipe in self.pipes:
                if pipe.is_colliding(bird):
                    self.over(bird)

    def over(self, bird):
        if not settings.AI:
            self.run = False

        else:
            i = self.birds.index(bird)
            self.ge[i].fitness -= 1
            self.birds.pop(i)
            self.nets.pop(i)
            self.ge.pop(i)

            if len(self.birds) == 0:
                self.run = False

    def reset(self, ai=False):
        self.pipes = []
        self.birds = []

        if not ai:
            settings.AI = messagebox.askyesno("AI?", "Would You Like To Use The AI?")

        if not settings.AI:
            bird = Bird(*self.bird_args)
            self.birds.append(bird)

if __name__ == "__main__":    
    g = Game()
    g.start()
