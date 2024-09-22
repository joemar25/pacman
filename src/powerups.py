# src/powerups
import pygame


class SpeedBoost:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


class FreezePotion:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 255), self.rect)
