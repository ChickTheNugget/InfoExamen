import pygame, sys
from pygame.locals import *
from random import randrange, random

pygame.init()

SIZE = 620
N_CELLS = 31
FPS = 25
DIM = SIZE // N_CELLS
font = pygame.font.SysFont("Arial", 16)
screen = pygame.display.set_mode((SIZE, SIZE))

pygame.display.set_caption("Pacman")
screen.fill("brown")

clock = pygame.time.Clock()
done = False
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Maze:
    def __init__(self):
        self.cells = {}
        for i in range(N_CELLS):
            for j in range(N_CELLS):
                if i % 10 == 0 or j % 10 == 0:
                    self.cells[(i, j)] = "f"
                else:
                    self.cells[(i, j)] = "w"
    def draw(self):
        for i in range(N_CELLS):

            for j in range(N_CELLS):
                if self.cells[(i, j)] == "w":
                    pygame.draw.rect(screen, "brown", (i * DIM, j * DIM, i * DIM + DIM, j * DIM + DIM), 0)

                elif self.cells[(i, j)] == "f":
                    pygame.draw.rect(screen, "white", (i * DIM, j * DIM, i * DIM + DIM, j * DIM + DIM), 0)
                    pygame.draw.circle(screen, "green", (i * DIM + DIM // 2, j * DIM + DIM // 2), 3, 0)
                    pygame.draw.circle(screen, "darkgreen", (i * DIM + DIM // 2, j * DIM + DIM // 2), 4, 1)

                else:
                    pygame.draw.rect(screen, "white", (i * DIM, j * DIM, i * DIM + DIM, j * DIM + DIM), 0)

    def is_valid(self, x, y):
        if not (x, y) in self.cells:
            return False
        if self.cells[(x, y)] == "f" or self.cells[(x, y)] == "r":
            return True
        else:
            return False


class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen, "blue", (self.x * DIM + DIM // 2, self.y * DIM + DIM // 2), DIM // 2, 0)
        pygame.draw.rect(screen, "blue", (self.x * DIM, self.y * DIM + DIM // 2
                                          , DIM
                                          , DIM // 2), 0)
        pygame.draw.rect(screen, "white", (self.x * DIM + DIM // 5
                                           , self.y * DIM + DIM - DIM // 4
                                           , DIM // 5
                                           , DIM // 4), 0)
        pygame.draw.rect(screen, "white", (self.x * DIM + 3 * DIM // 5
                                           , self.y * DIM + DIM - DIM // 4
                                           , DIM // 5
                                           , DIM // 4), 0)
        pygame.draw.circle(screen, "white", (self.x * DIM + DIM // 2, self.y * DIM + DIM // 2), DIM // 8, 0)
        pygame.draw.circle(screen, "white", (self.x * DIM + 3 * DIM // 4, self.y * DIM + DIM // 2), DIM // 8, 0)

    def move(self, m):
        while True:
            (dx, dy) = directions[randrange(0, 4)]
            if m.is_valid(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy
                break


class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True
        self.score = 0

    def draw(self):
        if self.is_alive:
            pygame.draw.circle(screen, "gold", (self.x * DIM + DIM // 2, self.y * DIM + DIM // 2), DIM // 2, 0)
            pygame.draw.circle(screen, "black", (self.x * DIM + DIM // 4, self.y * DIM + DIM // 4), DIM // 16, 0)
            pygame.draw.circle(screen, "black", (self.x * DIM + 3 * DIM // 4, self.y * DIM + DIM // 4), DIM // 16, 0)
            pygame.draw.ellipse(screen, "red", (self.x * DIM + DIM // 4, self.y * DIM + DIM // 2, DIM // 2, DIM // 4), 0)
        else:
            pygame.draw.circle(screen, "red", (self.x * DIM + DIM // 2, self.y * DIM + DIM // 2), DIM // 2, 0)
            pygame.draw.circle(screen, "black", (self.x * DIM + DIM // 4, self.y * DIM + DIM // 4), DIM // 16, 0)
            pygame.draw.circle(screen, "black", (self.x * DIM + 3 * DIM // 4, self.y * DIM + DIM // 4), DIM // 16, 0)
            pygame.draw.ellipse(screen, "gold", (self.x * DIM + DIM // 4, self.y * DIM + DIM // 2, DIM // 2, DIM // 4), 0)

    def collides_with(self, g):
        if self.x == g.x and self.y == g.y:
            return True
        else:
            return False

    def move(self, maze, dx, dy):
        if maze.is_valid(self.x + dx, self.y + dy):
            if maze.cells[(self.x + dx, self.y + dy)] == "f":
                self.score += 1
                maze.cells[(self.x + dx, self.y + dy)] = "r"
            self.x += dx
            self.y += dy
            return True
        else:
            return False


def get_random_pos(maze):
    if randrange(1, 2) == 1:
        x = randrange(1, 3) * 10
        y = randrange(1, 30)
        return x, y
    else:
        x = randrange(1, 30)
        y = randrange(1, 3) * 10
        return x, y


def still_some_food(maze):
    for i in range(N_CELLS):
        for j in range(N_CELLS):
            if maze.cells[i][j] == "f":
                return False
    return True


m = Maze()
p = Pacman(0, 0)
ghosts = []
for i in range(4):
    x, y = get_random_pos(m)
    ghosts.append(Ghost(x, y))


finished = 0

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if not finished or p.score == 232:
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                p.move(m, 0, -1)
            elif keys[K_s]:
                p.move(m, 0, 1)
            elif keys[K_a]:
                p.move(m, -1, 0)
            elif keys[K_d]:
                p.move(m, 1, 0)

    if not finished or p.score == 232:
        m.draw()

        for ghost in ghosts:
            ghost.draw()
            if p.collides_with(ghost):
                p.is_alive = False
                finished = 1
                continue
            ghost.move(m)
            
            
        p.draw()
    if finished:
        if p.score == 232:
            text = font.render(f"YOU WON! SCORE:{p.score}", True , "green")
        else:
            text = font.render(f"YOU DIED! SCORE:{p.score}", True , "orange")
        screen.blit(text, (SIZE // 2 - 65, SIZE // 2))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()