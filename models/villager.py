import random
import pygame
import settings
from settings import *


class Villager:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.name = random.choice(names)
        self.clan = None

    def draw(self, screen):
        color = self.clan.color if self.clan else (50, 50, 200)
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)

        name_surface = settings.game_font.render(self.name, True, TEXT_COLOR)
        name_rect = name_surface.get_rect(center=(self.x, self.y - self.size - 5))
        screen.blit(name_surface, name_rect)

    def is_clicked(self, pos):
        return ((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2) <= self.size ** 2