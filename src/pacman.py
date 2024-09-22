# src/pacman
import pygame
import time

pygame.init()

WIDTH, HEIGHT = 560, 620
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("arial", 24)


class Pacman:
    def __init__(self, maze):
        self.maze = maze
        self.rect = pygame.Rect(280, 460, 20, 20)
        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)
        self.speed = 2
        self.score = 0
        self.lives = 3
        self.power_mode = False
        self.power_mode_timer = 0
        self.powerup_duration = 7
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.speed_boost_duration = 5

    def update(self):
        self.move()
        self.eat_pellets()
        self.update_power_mode()
        self.update_speed_boost()

    def move(self):
        if self.can_move(self.next_direction):
            self.direction = self.next_direction
        if self.can_move(self.direction):
            self.rect.move_ip(self.direction * self.speed)
            self.teleport()
        else:
            self.adjust_position()

    def can_move(self, direction):
        temp_rect = self.rect.move(direction * self.speed)
        return not any(temp_rect.colliderect(wall) for wall in self.maze.walls)

    def adjust_position(self):
        self.rect.topleft = (round(self.rect.left / 20) *
                             20, round(self.rect.top / 20) * 20)

    def teleport(self):
        if self.rect.left < 0:
            self.rect.right = WIDTH
        elif self.rect.right > WIDTH:
            self.rect.left = 0

    def change_direction(self, key):
        direction_map = {
            pygame.K_LEFT: pygame.Vector2(-1, 0),
            pygame.K_RIGHT: pygame.Vector2(1, 0),
            pygame.K_UP: pygame.Vector2(0, -1),
            pygame.K_DOWN: pygame.Vector2(0, 1),
        }
        if key in direction_map:
            self.next_direction = direction_map[key]

    def eat_pellets(self):
        for pellet in self.maze.pellets[:]:
            if self.rect.colliderect(pellet.rect):
                self.maze.pellets.remove(pellet)
                self.score += 10
        for power_pellet in self.maze.power_pellets[:]:
            if self.rect.colliderect(power_pellet.rect):
                self.maze.power_pellets.remove(power_pellet)
                self.score += 50
                self.power_mode = True
                self.power_mode_timer = time.time()

    def update_power_mode(self):
        if self.power_mode and time.time() - self.power_mode_timer > self.powerup_duration:
            self.power_mode = False

    def update_speed_boost(self):
        if self.speed_boost and time.time() - self.speed_boost_timer > self.speed_boost_duration:
            self.speed_boost = False
            self.speed = 2

    def activate_speed_boost(self):
        self.speed_boost = True
        self.speed = 4
        self.speed_boost_timer = time.time()

    def reset_position(self):
        self.rect.topleft = (280, 460)
        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.rect.center, 10)
        label = font.render("P", True, BLACK)
        screen.blit(label, (self.rect.centerx - label.get_width() //
                    2, self.rect.centery - label.get_height() // 2))
