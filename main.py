import pygame
import sys
from src.game import Game

pygame.init()

WIDTH, HEIGHT = 560, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

if __name__ == "__main__":
    game = Game()
    game.run()
