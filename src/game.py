# src/game
import pygame
import sys
import random
import time
from .maze import Maze
from .pacman import Pacman
from .ghost import Ghost
from .powerups import SpeedBoost, FreezePotion

pygame.init()

WIDTH, HEIGHT = 560, 620
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)


class Game:
    def __init__(self):
        self.maze = Maze()
        self.pacman = Pacman(self.maze)
        self.ghosts = [
            Ghost(self.maze, "red", (280, 260)),
            Ghost(self.maze, "pink", (260, 280)),
            Ghost(self.maze, "blue", (280, 280)),
            Ghost(self.maze, "orange", (300, 280)),
        ]
        self.state = "menu"
        self.high_score = 0
        self.level = 1
        self.speed_boosts = []
        self.freeze_potions = []

    def reset(self):
        self.maze.reset()
        self.pacman = Pacman(self.maze)
        for ghost in self.ghosts:
            ghost.reset_position()
            ghost.speed = 2 + (self.level - 1) * 0.5
        self.spawn_powerups()

    def get_valid_powerup_positions(self):
        valid_positions = []
        for y, row in enumerate(self.maze.maze_layout):
            for x, cell in enumerate(row):
                if cell == '.':  # Only place powerups where dots are
                    valid_positions.append((x * 20 + 10, y * 20 + 10))
        return valid_positions

    def spawn_powerups(self):
        valid_positions = self.get_valid_powerup_positions()

        # Spawn 2 speed boosts
        for _ in range(2):
            if valid_positions:
                pos = random.choice(valid_positions)
                self.speed_boosts.append(SpeedBoost(pos[0], pos[1]))
                valid_positions.remove(pos)

        # Spawn 2 freeze potions
        for _ in range(2):
            if valid_positions:
                pos = random.choice(valid_positions)
                self.freeze_potions.append(FreezePotion(pos[0], pos[1]))
                valid_positions.remove(pos)

    def run(self):
        while True:
            if self.state == "menu":
                self.show_menu()
            elif self.state == "game":
                self.game_loop()
            elif self.state == "win":
                self.show_win_screen()
            elif self.state == "game_over":
                self.show_game_over()

    def show_menu(self):
        screen.fill(BLACK)
        title = font.render("PAC-MAN", True, YELLOW)
        start = font.render("Press SPACE to Start", True, WHITE)
        high_score = font.render(f"High Score: {self.high_score}", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2))
        screen.blit(high_score, (WIDTH // 2 -
                    high_score.get_width() // 2, HEIGHT * 2 // 3))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "game"
                self.reset()

    def game_loop(self):
        clock.tick(FPS)
        screen.fill(BLACK)
        self.maze.draw(screen)
        self.pacman.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)
        for boost in self.speed_boosts:
            boost.draw(screen)
        for potion in self.freeze_potions:
            potion.draw(screen)

        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.pacman.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))
        screen.blit(lives_text, (WIDTH - 100, HEIGHT - 40))
        screen.blit(level_text, (WIDTH // 2 -
                    level_text.get_width() // 2, HEIGHT - 40))

        if self.pacman.power_mode:
            power_time = int(self.pacman.powerup_duration -
                             (time.time() - self.pacman.power_mode_timer))
            power_text = font.render(f"Power: {power_time}", True, YELLOW)
            screen.blit(power_text, (10, HEIGHT - 70))

        if self.pacman.speed_boost:
            boost_time = int(self.pacman.speed_boost_duration -
                             (time.time() - self.pacman.speed_boost_timer))
            boost_text = font.render(f"Speed: {boost_time}", True, (0, 255, 0))
            screen.blit(boost_text, (WIDTH - 100, HEIGHT - 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.pacman.change_direction(event.key)

        self.pacman.update()
        for ghost in self.ghosts:
            ghost.update(self.pacman)

        self.check_powerup_collisions()

        if self.pacman.lives <= 0:
            self.high_score = max(self.high_score, self.pacman.score)
            self.state = "game_over"
        elif self.maze.is_level_complete():
            self.state = "win"

    def check_powerup_collisions(self):
        for boost in self.speed_boosts[:]:
            if self.pacman.rect.colliderect(boost.rect):
                self.speed_boosts.remove(boost)
                self.pacman.activate_speed_boost()

        for potion in self.freeze_potions[:]:
            if self.pacman.rect.colliderect(potion.rect):
                self.freeze_potions.remove(potion)
                for ghost in self.ghosts:
                    ghost.frozen = True
                    ghost.frozen_timer = time.time()

    def show_win_screen(self):
        screen.fill(BLACK)
        win_text = font.render("YOU WIN!", True, YELLOW)
        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
        next_level_text = font.render("Press SPACE to Continue", True, WHITE)
        screen.blit(
            win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 -
                    score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(next_level_text, (WIDTH // 2 -
                    next_level_text.get_width() // 2, HEIGHT * 2 // 3))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.level += 1
                self.reset()
                self.state = "game"

    def show_game_over(self):
        screen.fill(BLACK)
        game_over = font.render("GAME OVER", True, RED)
        score = font.render(f"Score: {self.pacman.score}", True, WHITE)
        restart = font.render("Press SPACE to Restart", True, WHITE)
        screen.blit(game_over, (WIDTH // 2 -
                    game_over.get_width() // 2, HEIGHT // 3))
        screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
        screen.blit(
            restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT * 2 // 3))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "menu"
