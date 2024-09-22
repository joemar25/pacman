# src/__init__.py

from .game import Game
from .maze import Maze
from .pacman import Pacman
from .ghost import Ghost
from .powerups import SpeedBoost, FreezePotion

__all__ = ["Game", "Maze", "Pacman", "Ghost", "SpeedBoost", "FreezePotion"]
