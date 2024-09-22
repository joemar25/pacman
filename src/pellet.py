# src/pellet
import pygame

WHITE = (255, 255, 255)


class Pellet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y - 2, 4, 4)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.rect.center, 2)


class PowerPellet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 4, y - 4, 8, 8)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.rect.center, 4)
