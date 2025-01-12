import random
import armory
import bestiary
from classes import Player, Room, Game
from colorama import Fore, init


# Welcome Text for Game
def welcome():
    print(
        Fore.RED
        + "                                                       D U N G E O N"
    )
    print(
        Fore.GREEN
        + """
    The village of Gotham has been terrorized by strange, deadly creatures for months now. Unable to endure any 
    longer, the villagers pooled their wealth and hired the most skilled adventurer they could find: you. After
    listening to their tale of woe, you agree to enter the labyrinth where most of the creatures seem to originate,
    and destroy the foul beasts. Armed with a Long-sword and a bundle of torches, you descend into the labyrinth, 
    ready to do battle....
    """
    )


def play_game():
    # Init makes sure that Colorama works on other OS
    init()

    adventurer = Player()
    current_game = Game(adventurer)
    current_game.room = generate_room()

    # Calls the welcome function prompt
    welcome()

    # Get player input
    input(f"{Fore.CYAN}Press ENTER to continue...")
    current_game.room.print_description()
    explore_labyrinth(current_game)


# Generate a room
def generate_room() -> Room:
    items = []
    monster = {}

    # There is a 25% chance that this room has an item
    if random.randint(1, 100) < 26:
        i = random.choice(
            list(armory.items.values())
        )  # Have to use value method to make use of randint
        items.append(i)

    # There a 25% chance that this room will contain a monster
    if random.randint(1, 100) < 26:
        monster = random.choice(bestiary.monsters)

    return Room(items, monster)


def explore_labyrinth(current_game: Game):
    while True:
        for i in current_game.room.items:
            print(f"{Fore.YELLOW}You see a {i['name']}")

        if current_game.room.monster:
            print(f"{Fore.RED}There is a {current_game.room.monster['name']} here!!!")

        player_input = input(f"{Fore.YELLOW}-> ").lower().strip()

        # Do something with player's input
        if player_input == "help":
            show_help()
            continue

        elif player_input == "look":
            current_game.room.print_description()
            continue

        elif player_input.startswith("get"):
            if not current_game.room.items:
                print("There is nothing to pick up")
                continue
            else:
                get_an_item(current_game, player_input)
                continue

        elif player_input == "inventory" or player_input == "inv":
            show_inventory(current_game)
            continue

        elif player_input.startswith("drop"):
            drop_an_item(current_game, player_input)
            continue

        elif player_input.startswith("equip"):
            use_item(current_game.player, player_input[6:])
            continue

        elif player_input.startswith("use"):
            use_item(current_game.player, player_input[4:])
            continue

        elif player_input.startswith("unequip"):
            unequip_item(current_game.player, player_input[8:])
            continue

        # Moving around the map
        elif player_input in ["n", "s", "e", "w"]:
            print(f"{Fore.GREEN}You move deeper into the dungeon.")

        elif player_input == "status":
            print_status(current_game)
            continue

        # Quit the game
        elif player_input == "quit":
            print(f"{Fore.GREEN}Overcome with terror, you flee the dungeon.")
            # TODO: Print out the final score
            play_again()

        # Default case
        else:
            print(f"{Fore.GREEN}I'm not sure what you mean... type 'help' for help.")

        current_game.room = generate_room()
        current_game.room.print_description()
        current_game.player.turns = current_game.player.turns + 1


def print_status(current_game: Game):
    print(Fore.CYAN)
    print(
        f"You have played the game for {current_game.player.turns} turn(s), "
        + f"defeated {current_game.player.monsters_defeated} monsters, "
        + f"and found {current_game.player.treasure} gold pieces."
    )
    print(f"XP: {current_game.player.xp} xp.")
    print(f"Current HP: {current_game.player.hp}/100.")
    print(f"Currently equipped weapon: {current_game.player.current_weapon['name']}")
    print(f"Currently equipped shield: {current_game.player.current_shield['name']}")
    print(f"Currently equipped armor: {current_game.player.current_armor['name']}")


def unequip_item(player: Player, item: str):
    if item in player.inventory:
        # Is the item equipped?
        if player.current_weapon["name"] == item:
            player.current_weapon = armory.default["hands"]
            print(f"{Fore.CYAN}You stopped using the {item}.")
        elif player.current_armor["name"] == item:
            player.current_armor = armory.default["clothes"]
            print(f"{Fore.CYAN}You stopped using the {item}.")
        elif player.current_shield["name"] == item:
            player.current_shield = armory.default["no shield"]
            print(f"{Fore.CYAN}You stopped using the {item}.")
        else:
            print(f"{Fore.RED}You don't have a {item}.")
    else:
        print(f"{Fore.RED}You don't have a {item}.")


def use_item(player: Player, item: str):
    if item in player.inventory:
        old_weapon = player.current_weapon

        if armory.items[item]["type"] == "weapon":
            player.current_weapon = armory.items[item]
            print(
                f"{Fore.CYAN}You arm yourself with a {player.current_weapon['name']} instead of your {old_weapon['name']}."
            )

            if item == "longbow" and player.current_shield["name"] != "no shield":
                player.current_shield = -armory.default["no shield"]
                print(
                    f"Since you cannot use a shield with a {item}, you sling it over your back."
                )

        elif armory.items[item]["type"] == "armor":
            player.current_armor = armory.items[item]
            print(f"{Fore.CYAN}You put on the {player.current_armor['name']}.")

        elif armory.items[item]["type"] == "shield":
            # You can't use a shield with a bow
            if player.current_weapon["name"] == "longbow":
                print(f"{Fore.RED}You can't use a shield while you are using a bow!!!")
            else:
                player.current_shield = armory.items[item]
                print(f"{Fore.CYAN}You equip your {player.current_shield['name']}.")

        else:
            print(f"{Fore.RED}You can't use a {item} as armor, weapon, or shield.")

    else:
        print(f"{Fore.RED}You don't have a {item}.")


def drop_an_item(current_game: Game, player_input: str):
    if player_input[5:] == current_game.player.current_weapon["name"]:
        print(f"{Fore.RED}You cannot drop your currently equipped weapon!")
    elif player_input[5:] == current_game.player.current_armor["name"]:
        print(f"{Fore.RED}You cannot drop your currently equipped armor!")
    elif player_input[5:] == current_game.player.current_shield["name"]:
        print(f"{Fore.RED}You cannot drop your currently equipped shield!")
    else:
        try:
            current_game.player.inventory.remove(player_input[5:])
            print(f"{Fore.CYAN}You drop the {player_input[5:]}.")
            current_game.room.items.append(armory.items[player_input[5:]])
        except ValueError:
            print(f"{Fore.RED}You are not carrying a {player_input[5:]}.")


def show_inventory(current_game: Game):
    print(f"{Fore.CYAN}Your inventory:")
    print(f"    - {current_game.player.treasure} pieces of gold.")

    for x in current_game.player.inventory:
        if x == current_game.player.current_weapon["name"]:
            print(f"    - {x.capitalize()} (equipped).")
        elif x == current_game.player.current_armor["name"]:
            print(f"    - {x.capitalize()} (equipped).")
        elif x == current_game.player.current_shield["name"]:
            print(f"    - {x.capitalize()} (equipped).")
        else:
            print(f"    - {x.capitalize()}")


def get_an_item(current_game, player_input):
    if len(current_game.room.items) > 0 and player_input[4:] == "":
        player_input = player_input + " " + current_game.room.items[0]["name"]

    if player_input[4:] not in current_game.player.inventory:
        # Add to inventory
        idx = find_in_list(player_input[4:], "name", current_game.room.items)

        if idx > -1:
            cur_item = current_game.room.items[idx]
            current_game.player.inventory.append(cur_item["name"])
            current_game.room.items.pop(idx)
            print(f"{Fore.CYAN}You picked up the {cur_item['name']}.")
        else:
            print(f"{Fore.RED}There is no {player_input[4:]} here!")

    else:
        print(
            f"{Fore.YELLOW}You already have a {player_input[4:]}, and decide you don't need another one."
        )


def find_in_list(search_string: str, key: str, list_to_search: list) -> int:
    idx = -1
    count = 0
    for item in list_to_search:
        if item[key] == search_string:
            idx = count
        count = count + 1
    return idx


def play_again():
    # Yes/No user input. Calls get_yn function.
    yn = get_yn(Fore.YELLOW + "Do you want to play again? ")

    if yn == "yes":
        play_game()
    else:
        print("Until next time.")
        exit(0)


def get_yn(question: str) -> str:
    while True:
        answer = input(question + "(Yes/No) -> ").lower().strip()

        if answer not in ["yes", "no", "y", "n"]:
            print("Please enter yes or no...")
        else:
            if answer == "y":
                answer = "yes"
            elif answer == "n":
                answer = "no"
            return answer


def show_help():
    print(
        Fore.GREEN
        + """Enter a command:
          - N/S/E/W - Move in a direction
          - Map - Show a map of the labyrinth
          - Look - Look around and describe your environment
          - Equip <item> - Use an item from your inventory
          - Un-equip <item> - Stop using an item from your inventory
          - Fight - Attack your enemy
          - Examine <object> - Examine an object
          - Get <item> - Pick up an item
          - Drop <item> - Drop an item
          - Rest - Restore your health
          - Inventory - Show your inventory
          - Status - Show current player status
          - Quit - Quit the game
    """
    )
