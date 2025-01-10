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

    # Room
    room = Room()
    room.description = "This is an empty room."
    room.sound = "You hear water dripping."
    room.smell = "There is an musty smell in the air."

    # Current Game
    current_game.room = room

    # Calls the welcome function prompt
    welcome()

    # Get player input
    input("Press ENTER to continue...")
    explore_labyrinth(current_game)


def explore_labyrinth(current_game: Game):
    while True:
        current_game.room.print_description()

        player_input = input(Fore.YELLOW + "-> ").lower().strip()

        # Do something with player's input
        if player_input == "help":
            show_help()
        elif player_input == "quit":
            print("Overcome with terror, you flee the dungeon.")
            # TODO: Print out the final score
            play_again()
        else:
            print("I'm not sure what you mean... type 'help' for help.")


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
