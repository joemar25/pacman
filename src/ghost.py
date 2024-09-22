# src/ghost
import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 560, 620
BLACK = (0, 0, 0)

GHOST_COLORS = {
    "red": (255, 0, 0),
    "pink": (255, 192, 203),
    "blue": (0, 191, 255),
    "orange": (255, 165, 0),
}

font = pygame.font.SysFont("arial", 24)


class Ghost:
    def __init__(self, maze, color, position):
        self.maze = maze
        self.color_name = color
        self.color = GHOST_COLORS[color]
        self.rect = pygame.Rect(position[0], position[1], 20, 20)
        self.direction = random.choice([pygame.Vector2(
            1, 0), pygame.Vector2(-1, 0), pygame.Vector2(0, 1), pygame.Vector2(0, -1)])
        self.speed = 2
        self.scared = False
        self.spawn_position = self.rect.center
        self.state = "chase"
        self.state_timer = 0
        self.frozen = False
        self.frozen_timer = 0
        self.frozen_duration = 3

    def update(self, pacman):
        if self.frozen:
            if time.time() - self.frozen_timer > self.frozen_duration:
                self.frozen = False
            return

        self.scared = pacman.power_mode
        self.update_state()
        self.move(pacman)
        self.check_collision(pacman)

    def update_state(self):
        current_time = time.time()
        if current_time - self.state_timer > 20:
            self.state = "scatter" if self.state == "chase" else "chase"
            self.state_timer = current_time

    def move(self, pacman):
        if not self.can_move(self.direction) or random.random() < 0.02:
            self.choose_direction(pacman)
        self.rect.move_ip(self.direction * self.speed)
        self.teleport()

    def choose_direction(self, pacman):
        possible_directions = [pygame.Vector2(
            1, 0), pygame.Vector2(-1, 0), pygame.Vector2(0, 1), pygame.Vector2(0, -1)]
        valid_directions = [d for d in possible_directions if self.can_move(d)]

        if self.scared:
            self.direction = random.choice(valid_directions)
        else:
            if self.state == "chase":
                target = pacman.rect.center
            else:
                target = self.get_scatter_target()

            self.direction = min(
                valid_directions,
                key=lambda d: pygame.Vector2(self.rect.center).distance_to(
                    pygame.Vector2(self.rect.center) + d * 20)
                + pygame.Vector2(self.rect.center + d *
                                 20).distance_to(target),
            )

    def get_scatter_target(self):
        scatter_targets = {
            "red": (WIDTH - 20, 0),
            "pink": (20, 0),
            "blue": (WIDTH - 20, HEIGHT - 20),
            "orange": (20, HEIGHT - 20),
        }
        return scatter_targets[self.color_name]

    def teleport(self):
        if self.rect.left < 0:
            self.rect.right = WIDTH
        elif self.rect.right > WIDTH:
            self.rect.left = 0

    def can_move(self, direction):
        temp_rect = self.rect.move(direction * self.speed)
        return not any(temp_rect.colliderect(wall) for wall in self.maze.walls)

    def check_collision(self, pacman):
        if self.rect.colliderect(pacman.rect):
            if self.scared:
                self.reset_position()
                pacman.score += 200
            else:
                pacman.lives -= 1
                pacman.reset_position()
                self.reset_position()
                pygame.time.wait(1000)

    def reset_position(self):
        self.rect.center = self.spawn_position
        self.direction = pygame.Vector2(0, -1)
        self.state = "chase"
        self.state_timer = time.time()

    def draw(self, screen):
        color = (100, 100, 255) if self.scared else self.color
        if self.frozen:
            color = (200, 200, 255)
        pygame.draw.rect(screen, color, self.rect)
        label = font.render(self.color_name[0].upper(), True, BLACK)
        screen.blit(label, (self.rect.centerx - label.get_width() //
                    2, self.rect.centery - label.get_height() // 2))
