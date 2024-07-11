import sys
import pygame
import settings
from settings import *
from models.village import Village


class VillageSimulation:
    def __init__(self):
        self.SAVE_EVENT = None
        self.WARFARE_EVENT = None
        self.BIRTH_EVENT = None
        pygame.init()
        settings.game_font = pygame.font.Font(None, 20)
        settings.sidebar_font = pygame.font.Font(None, 24)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Clan Warfare Game")

        self.village = Village()
        self.village.load_game()

        self.setup_events()
        self.selected_villager = None
        self.running = True
        self.clock = pygame.time.Clock()

    def setup_events(self):
        self.BIRTH_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRTH_EVENT, 10)

        self.WARFARE_EVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.WARFARE_EVENT, 100)

        self.SAVE_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(self.SAVE_EVENT, 1000)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.village.save_game()
                self.running = False
            elif event.type == self.BIRTH_EVENT:
                self.village.add_villager()
            elif event.type == self.WARFARE_EVENT:
                self.village.clan_warfare()
            elif event.type == self.SAVE_EVENT:
                self.village.save_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.selected_villager = self.village.get_clicked_villager(event.pos)

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.village.draw(self.screen)
        self.draw_sidebar()

    def draw_sidebar(self):
        pygame.draw.rect(self.screen, SIDEBAR_COLOR, (main_width, 0, sidebar_width, height))

        if self.selected_villager:
            info_text = [
                f"Name: {self.selected_villager.name}",
                f"Clan: {'Yes' if self.selected_villager.clan else 'No'}",
                f"Clan Size: {self.selected_villager.clan.size() if self.selected_villager.clan else 'N/A'}",
                f"Clan Strength: {self.selected_villager.clan.strength if self.selected_villager.clan else 'N/A'}"
            ]
            for i, text in enumerate(info_text):
                info_surface = settings.sidebar_font.render(text, True, TEXT_COLOR)
                info_rect = info_surface.get_rect(topleft=(main_width + 10, 10 + i * 30))
                self.screen.blit(info_surface, info_rect)

        total_info = [
            f"Total Villagers: {self.village.total_number_of_villagers}",
            f"Current Villagers: {len(self.village.villagers)}",
            f"Total Clans: {len(self.village.clans)}",
            f"Dead Clans: {len(self.village.perished_clans)}",
            f"Largest clan: {max(self.village.clans, key=lambda value: value.size()).size()}",
            f"Smallest clan: {min(self.village.clans, key=lambda value: value.size()).size()}"
        ]
        for i, text in enumerate(total_info):
            info_surface = settings.sidebar_font.render(text, True, TEXT_COLOR)
            info_rect = info_surface.get_rect(topleft=(main_width + 10, height - 30 * len(total_info) + i * 30))
            self.screen.blit(info_surface, info_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    simulation = VillageSimulation()
    simulation.run()
