"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/connect_four
    Mateusz Olstowski

-------------------------------

Rules:
    https://en.wikipedia.org/wiki/Connect_Four
    variant: PopOut

    Rules are easy. You must be the first who form a
    horizontal, vertical, or diagonal line of four of one's own tokens.

Run game:
    To run the program you need python 3.
    Install the required packages
    and run main.py.
    How to do this can be found in the README

-------------------------------

Conclusions:
    (Jakub)
    Bot_level (depth) - how many moves in advance should the AI think

    AI vs AI
    --------
    Both artificial intelligences maintain a similar starting pattern,
    they try to fill the first and second columns.

    player vs AI
    ------------
    Against the player, the AI first tries to fill the first row, but when it sees it
    the player is close to victory, he blocks the winning move.

    So,
    I believe that with more advanced algorithms the game would be much more difficult.

"""

from classes.create_game import CreateGame


def main():
    new_game = CreateGame()
    new_game.start_game()


if __name__ == "__main__":
    main()
