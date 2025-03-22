import random

from classes import Game
from colorama import Fore
import config as cfg
from util import get_yn

from time import sleep


def fight(current_game: Game) -> str:
    rm = current_game.room
    player = current_game.player

    # assume the player goes first
    players_turn = True

    # roll for initiative, or flip a coin
    if random.randint(1, 2) == 2:
        players_turn = False

    if players_turn:
        print(f"{Fore.CYAN}You brace yourself and attack the {rm.monster['name']}.")
    else:
        print(f"{Fore.CYAN}The {rm.monster['name']} moves quickly and attacks first!")

    # get the monster's hit points
    monster_hp = random.randint(rm.monster["min_hp"], rm.monster["max_hp"])
    monster_original_hp = monster_hp

    winner = ""

    while True:
        if players_turn:
            my_roll = random.randint(1, 100)

            # we modify the player's roll by adding the "to_hit" attribute for the currently equipped weapon,
            # and subtracting the monster's "armor_modifier." Note that subtracting a negative number
            # is the same as adding a positive version of that number.
            modified_roll = my_roll + player.current_weapon['to_hit'] - rm.monster['armor_modifier']

            # 50% chance to hit
            if modified_roll > 50:
                print(f"{Fore.GREEN}You hit the {rm.monster['name']} with your {player.current_weapon['name']}!")
                monster_hp = monster_hp - random.randint(player.current_weapon['min_damage'],
                                                         player.current_weapon['max_damage'])
            else:
                print(f"{Fore.GREEN}You attack the {rm.monster['name']} and miss!")

            if monster_hp <= 0:
                print(f"{Fore.GREEN}The {rm.monster['name']} falls to the floor, dead.")
                winner = "player"
        else:
            # monster's turn
            monster_roll = random.randint(1, 100)

            # we modify the monster's attack roll by subtracting the "defense" attribute for the player's currently
            # equipped weapon and armor
            modified_monster_roll = monster_roll - (player.current_shield['defense'] + player.current_armor['defense'])

            if modified_monster_roll > 50:
                print(f"{Fore.RED}The {rm.monster['name']} attacks and hits!")
                player.hp = player.hp - random.randint(rm.monster['min_damage'], rm.monster['max_damage'])
            else:
                print(f"{Fore.GREEN}The {rm.monster['name']} attacks and misses!")

            if player.hp <= 0:
                print(f"{Fore.RED}The {rm.monster['name']} kills you, and you fall to the floor, dead.")
                winner = "monster"

        # check to see if someone died; if so, the battle is over
        if player.hp <= 0 or monster_hp <= 0:
            break

        # let the player know how the monster is doing
        if monster_hp < monster_original_hp / 2:
            print(f"{Fore.YELLOW}The {rm.monster['name']} is bleeding profusely.")
        elif monster_hp < monster_original_hp / 3:
            print(f"{Fore.YELLOW}The {rm.monster['name']} is bleeding profusely, and looks to be nearly dead.")

        # give the player a warning and a chance to run away if they are badly wounded
        if player.hp <= int(0.2 * cfg.PLAYER_HP):
            answer = get_yn(f"{Fore.RED}You are near death. Do you want to continue?")
            if answer == "no":
                return "flee"

        elif player.hp <= int(0.3 * cfg.PLAYER_HP):
            answer = get_yn(f"{Fore.RED}You are badly wounded. Do you want to continue?")
            if answer == "no":
                return "flee"

        elif player.hp <= int(0.5 * cfg.PLAYER_HP):
            answer = get_yn(f"{Fore.RED}You are lightly wounded. Do you want to continue?")
            if answer == "no":
                return "flee"

        elif player.hp < cfg.PLAYER_HP:
            print("You are only lightly wounded. 'Tis but a scratch.")

        sleep(1)
        print(f"{Fore.GREEN}")

        players_turn = not players_turn

    return winner
