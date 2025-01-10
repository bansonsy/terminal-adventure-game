import game


def main():
    # Print a welcome screen
    game.welcome()

    # Play the game until the game is over or til the player quits
    while True:
        game.play_game()


if __name__ == "__main__":
    main()
