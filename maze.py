import pygame
from pellet import Pellet, PowerPellet

pygame.init()

WIDTH, HEIGHT = 560, 620
BLUE = (0, 0, 255)


class Maze:
    def __init__(self):
        self.maze_layout = [
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
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        self.create_maze()

    def create_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, col in enumerate(row):
                position = pygame.Rect(x * 20, y * 20, 20, 20)
                if col == "#":
                    self.walls.append(position)
                elif col == ".":
                    self.pellets.append(Pellet(x * 20 + 10, y * 20 + 10))
                elif col == "o":
                    self.power_pellets.append(
                        PowerPellet(x * 20 + 10, y * 20 + 10))

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall)
        for pellet in self.pellets:
            pellet.draw(screen)
        for power_pellet in self.power_pellets:
            power_pellet.draw(screen)

    def reset(self):
        self.walls.clear()
        self.pellets.clear()
        self.power_pellets.clear()
        self.create_maze()

    def is_level_complete(self):
        return len(self.pellets) == 0 and len(self.power_pellets) == 0
