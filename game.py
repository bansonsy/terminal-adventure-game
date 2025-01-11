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

    # Calls the welcome function prompt
    welcome()

    # Get player input
    input("Press ENTER to continue...")
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
        room = generate_room()
        current_game.room = room
        current_game.room.print_description()

        for i in current_game.room.items:
            print(f"{Fore.YELLOW}You see a {i['name']}")

        if current_game.room.monster:
            print(f"{Fore.RED}There is a {current_game.room.monster['name']} here!!!")

        player_input = input(Fore.YELLOW + "-> ").lower().strip()

        # Do something with player's input
        if player_input == "help":
            show_help()

        elif player_input.startswith("get"):
            if not current_game.room.items:
                print("There is nothing to pick up")
                continue
            else:
                get_an_item(current_game, player_input)

        elif player_input in ["n", "s", "e", "w"]:
            print(f"{Fore.GREEN}You move deeper into the dungeon.")
            continue

        # Quit the game
        elif player_input == "quit":
            print("Overcome with terror, you flee the dungeon.")
            # TODO: Print out the final score
            play_again()

        # Default case
        else:
            print("I'm not sure what you mean... type 'help' for help.")


def get_an_item(current_game, player_input):
    pass


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
