import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 560, 620
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

GHOST_COLORS = {
    "red": (255, 0, 0),
    "pink": (255, 192, 203),
    "blue": (0, 191, 255),
    "orange": (255, 165, 0),
}

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# Maze Layout
maze_layout = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "     #.## ###--### ##.#     ",
    "######.## #      # ##.######",
    "      .   #      #   .      ",
    "######.## #      # ##.######",
    "     #.## ######## ##.#     ",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]


# Maze class definition
class Maze:
    def __init__(self):
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        self.create_maze()

    def create_maze(self):
        """Create walls, pellets, and power pellets based on maze layout."""
        for y, row in enumerate(maze_layout):
            for x, col in enumerate(row):
                position = pygame.Rect(x * 20, y * 20, 20, 20)
                if col == "#":
                    self.walls.append(position)
                elif col == ".":
                    self.pellets.append(Pellet(x * 20 + 10, y * 20 + 10))
                elif col == "o":
                    self.power_pellets.append(PowerPellet(x * 20 + 10, y * 20 + 10))

    def draw(self, screen):
        """Draw walls, pellets, and power pellets."""
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall)
        for pellet in self.pellets:
            pellet.draw(screen)
        for power_pellet in self.power_pellets:
            power_pellet.draw(screen)

    def reset(self):
        """Reset the maze by clearing and recreating all entities."""
        self.walls.clear()
        self.pellets.clear()
        self.power_pellets.clear()
        self.create_maze()

    def is_level_complete(self):
        """Check if all pellets and power pellets are collected."""
        return len(self.pellets) == 0 and len(self.power_pellets) == 0


# Pacman class definition
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

    def update(self):
        """Update Pacman's position and actions."""
        self.move()
        self.eat_pellets()
        self.update_power_mode()

    def move(self):
        """Move Pacman based on current direction and check for collisions."""
        if self.can_move(self.next_direction):
            self.direction = self.next_direction
        if self.can_move(self.direction):
            self.rect.move_ip(self.direction * self.speed)
            self.teleport()
        else:
            self.adjust_position()

    def can_move(self, direction):
        """Check if Pacman can move in the given direction."""
        temp_rect = self.rect.move(direction * self.speed)
        return not any(temp_rect.colliderect(wall) for wall in self.maze.walls)

    def adjust_position(self):
        """Adjust Pacman's position to avoid getting stuck in walls."""
        self.rect.topleft = (
            round(self.rect.left / 20) * 20,
            round(self.rect.top / 20) * 20,
        )

    def teleport(self):
        """Handle Pacman teleportation across the screen edges."""
        if self.rect.left < 0:
            self.rect.right = WIDTH
        elif self.rect.right > WIDTH:
            self.rect.left = 0

    def change_direction(self, key):
        """Handle user input to change Pacman's direction."""
        direction_map = {
            pygame.K_LEFT: pygame.Vector2(-1, 0),
            pygame.K_RIGHT: pygame.Vector2(1, 0),
            pygame.K_UP: pygame.Vector2(0, -1),
            pygame.K_DOWN: pygame.Vector2(0, 1),
        }
        if key in direction_map:
            self.next_direction = direction_map[key]

    def eat_pellets(self):
        """Handle Pacman eating pellets and power pellets."""
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
        """Update Pacman's power mode based on the timer."""
        if self.power_mode and time.time() - self.power_mode_timer > 7:
            self.power_mode = False

    def reset_position(self):
        """Reset Pacman's position to the start position."""
        self.rect.topleft = (round(280 / 20) * 20, round(460 / 20) * 20)
        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)

    def draw(self, screen):
        """Draw Pacman on the screen."""
        pygame.draw.circle(screen, YELLOW, self.rect.center, 10)


# Ghost class definition (enemies)
class Ghost:
    def __init__(self, maze, color, position):
        self.maze = maze
        self.color_name = color
        self.color = GHOST_COLORS[color]
        self.rect = pygame.Rect(position[0], position[1], 20, 20)
        self.direction = random.choice(
            [
                pygame.Vector2(1, 0),
                pygame.Vector2(-1, 0),
                pygame.Vector2(0, 1),
                pygame.Vector2(0, -1),
            ]
        )
        self.speed = 2
        self.scared = False
        self.spawn_position = self.rect.center
        self.state = "chase"
        self.state_timer = 0

    def update(self, pacman):
        """Update ghost behavior based on game state and Pacman."""
        self.scared = pacman.power_mode
        self.update_state()
        self.move(pacman)
        self.check_collision(pacman)

    def update_state(self):
        """Toggle between chase and scatter mode periodically."""
        current_time = time.time()
        if current_time - self.state_timer > 20:
            self.state = "scatter" if self.state == "chase" else "chase"
            self.state_timer = current_time

    def move(self, pacman):
        """Move the ghost based on its current state and position."""
        if not self.can_move(self.direction) or random.random() < 0.02:
            self.choose_direction(pacman)
        self.rect.move_ip(self.direction * self.speed)
        self.teleport()

    def choose_direction(self, pacman):
        """Choose a new direction for the ghost."""
        possible_directions = [
            pygame.Vector2(1, 0),
            pygame.Vector2(-1, 0),
            pygame.Vector2(0, 1),
            pygame.Vector2(0, -1),
        ]
        valid_directions = [d for d in possible_directions if self.can_move(d)]

        if self.scared:
            self.direction = random.choice(valid_directions)
        else:
            if self.state == "chase":
                target = pacman.rect.center
            else:  # scatter mode
                target = self.get_scatter_target()

            self.direction = min(
                valid_directions,
                key=lambda d: pygame.Vector2(self.rect.center).distance_to(
                    pygame.Vector2(self.rect.center) + d * 20
                )
                + pygame.Vector2(self.rect.center + d * 20).distance_to(target),
            )

    def get_scatter_target(self):
        """Get the scatter target based on the ghost's color."""
        scatter_targets = {
            "red": (WIDTH - 20, 0),
            "pink": (20, 0),
            "blue": (WIDTH - 20, HEIGHT - 20),
            "orange": (20, HEIGHT - 20),
        }
        return scatter_targets[self.color_name]

    def teleport(self):
        """Handle ghost teleportation across the screen edges."""
        if self.rect.left < 0:
            self.rect.right = WIDTH
        elif self.rect.right > WIDTH:
            self.rect.left = 0

    def can_move(self, direction):
        """Check if the ghost can move in the given direction."""
        temp_rect = self.rect.move(direction * self.speed)
        return not any(temp_rect.colliderect(wall) for wall in self.maze.walls)

    def check_collision(self, pacman):
        """Check if the ghost collides with Pacman."""
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
        """Reset the ghost to its spawn position."""
        self.rect.center = self.spawn_position
        self.direction = pygame.Vector2(0, -1)
        self.state = "chase"
        self.state_timer = time.time()

    def draw(self, screen):
        """Draw the ghost on the screen."""
        color = (100, 100, 255) if self.scared else self.color
        pygame.draw.rect(screen, color, self.rect)


# Pellet class definition
class Pellet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y - 2, 4, 4)

    def draw(self, screen):
        """Draw pellet on the screen."""
        pygame.draw.circle(screen, WHITE, self.rect.center, 2)


# PowerPellet class definition
class PowerPellet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 4, y - 4, 8, 8)

    def draw(self, screen):
        """Draw power pellet on the screen."""
        pygame.draw.circle(screen, WHITE, self.rect.center, 4)


# Game class definition
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
        self.level = 1  # Level tracking

    def reset(self):
        """Reset the game for the next level."""
        self.maze.reset()
        self.pacman = Pacman(self.maze)
        for ghost in self.ghosts:
            ghost.reset_position()
            ghost.speed = 2 + (self.level - 1) * 0.5  # Increase speed per level

    def run(self):
        """Run the main game loop."""
        while True:
            if self.state == "menu":
                self.show_menu()
            elif self.state == "game":
                self.game_loop()
            elif self.state == "win":
                self.show_win_screen()  # Handle win state
            elif self.state == "game_over":
                self.show_game_over()

    def show_menu(self):
        """Show the game menu."""
        screen.fill(BLACK)
        title = font.render("PAC-MAN", True, YELLOW)
        start = font.render("Press SPACE to Start", True, WHITE)
        high_score = font.render(f"High Score: {self.high_score}", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2))
        screen.blit(
            high_score, (WIDTH // 2 - high_score.get_width() // 2, HEIGHT * 2 // 3)
        )
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
        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.pacman.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))
        screen.blit(lives_text, (WIDTH - 100, HEIGHT - 40))
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT - 40))
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

        if self.pacman.lives <= 0:
            self.high_score = max(self.high_score, self.pacman.score)
            self.state = "game_over"
        elif self.maze.is_level_complete():
            self.state = "win"  # Transition to win state

    def show_win_screen(self):
        screen.fill(BLACK)
        win_text = font.render("YOU WIN!", True, YELLOW)
        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
        next_level_text = font.render("Press SPACE to Continue", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(
            next_level_text,
            (WIDTH // 2 - next_level_text.get_width() // 2, HEIGHT * 2 // 3),
        )
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
        """Show the game over screen."""
        screen.fill(BLACK)
        game_over = font.render("GAME OVER", True, RED)
        score = font.render(f"Score: {self.pacman.score}", True, WHITE)
        restart = font.render("Press SPACE to Restart", True, WHITE)
        screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 3))
        screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT * 2 // 3))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "menu"


if __name__ == "__main__":
    game = Game()
    game.run()
