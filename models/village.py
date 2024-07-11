import math
import os
import pickle
import random

from models.clan import Clan
from models.villager import Villager
from settings import *


class Village:
    def __init__(self):
        self.villagers = []
        self.clans = []
        self.perished_clans = []
        self.total_number_of_villagers = 0

    def add_villager(self):
        self.total_number_of_villagers += 1
        x = random.randint(0, main_width)
        y = random.randint(0, height)
        new_villager = Villager(x, y)

        # Check for nearby villagers to form or join a clan
        for villager in self.villagers:
            distance = math.hypot(new_villager.x - villager.x, new_villager.y - villager.y)
            if distance < 50:  # Clan formation distance
                if villager.clan:
                    new_villager.clan = villager.clan
                    villager.clan.members.append(new_villager)
                else:
                    new_clan = Clan()
                    new_clan.members.extend([villager, new_villager])
                    villager.clan = new_clan
                    new_villager.clan = new_clan
                    self.clans.append(new_clan)
                break

        self.villagers.append(new_villager)

    def draw(self, screen):
        for villager in self.villagers:
            villager.draw(screen)

    def get_clicked_villager(self, pos):
        for villager in self.villagers:
            if villager.is_clicked(pos):
                return villager
        return None

    @staticmethod
    def calculate_battle_result(clan1: Clan, clan2: Clan):
        # Introduce a random luck factor
        luck_factor = random.uniform(0.8, 1.2)  # Random value between 0.8 and 1.2

        # Calculate adjusted strengths
        adjusted_clan1_strength = clan1.strength * luck_factor
        adjusted_clan2_strength = clan2.strength * luck_factor

        if adjusted_clan1_strength > adjusted_clan2_strength:
            winner, loser = clan1, clan2
        else:
            winner, loser = clan2, clan1

        return winner, loser

    def clan_warfare(self):
        if len(self.clans) < 2:
            return

        # Find clans large enough to fight
        fighting_clans = [clan for clan in self.clans if clan.size() >= 5]

        if len(fighting_clans) >= 2:
            clan1, clan2 = random.sample(fighting_clans, 2)

            # Determine the winner based on total strength
            winner, loser = self.calculate_battle_result(clan1, clan2)

            # Remove the losing clan
            self.clans.remove(loser)
            self.perished_clans.append(loser)
            for member in loser.members:
                self.villagers.remove(member)

            # Notify about the battle
            print(f"Clan battle! Clan of size {winner.size()} defeated clan of size {loser.size()}!")

    def save_game(self):
        game_state = {
            'villagers': self.villagers,
            'clans': self.clans
        }
        with open('../village_sim_save.pkl', 'wb') as f:
            pickle.dump(game_state, f)
        print("Game saved!")

    def load_game(self):
        if os.path.exists('../village_sim_save.pkl'):
            with open('../village_sim_save.pkl', 'rb') as f:
                game_state = pickle.load(f)
            self.villagers = game_state['villagers']
            self.clans = game_state['clans']
            # Restore clan references for villagers
            for clan in self.clans:
                for villager in clan.members:
                    villager.clan = clan
            print("Game loaded!")
