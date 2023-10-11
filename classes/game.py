import numpy as np
from easyAI import TwoPlayerGame


class Game(TwoPlayerGame):
    def __init__(self, players):
        self.__rows = 6
        self.__cols = 7
        self.players = players
        self.__board = self._create_board()
        print(type(self.__board))
        self.current_player = 1

    def _create_board(self):
        """
        Creates game board

        Returns
        -------
            array: list - List of list with strings
        """
        return np.zeros((self.__rows, self.__cols), dtype=str)

    def _pos_dir(self):
        """
        Returns an array of positions with a possibly found streak

        Returns
        -------
            array: list - list of positions with a possibly found streak
        """
        # TODO try find another way
        return np.array(
            [[[i, 0], [0, 1]] for i in range(6)]
            + [[[0, i], [1, 0]] for i in range(7)]
            + [[[i, 0], [1, 1]] for i in range(1, 3)]
            + [[[0, i], [1, 1]] for i in range(4)]
            + [[[i, 6], [1, -1]] for i in range(1, 3)]
            + [[[0, i], [1, -1]] for i in range(3, 7)]
        )

    def _find_four(self):
        """
        Returns whether any player has a streak or not

        Returns
        -------
            value: bool - Whether any player has a streak or not
        """
        for pos, direction in self._pos_dir():
            streak = 0
            while (0 <= pos[0] < self.__rows) and (0 <= pos[1] < self.__cols):
                if self.__board[pos[0], pos[1]] == self._get_current_player_character(
                    self.opponent_index
                ):
                    streak += 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
                pos = pos + direction
        return False

    def _get_current_player_character(self, player_index: int) -> str:
        """
        Returns the current player's character

        Parameters
        ----------
            player_index: int - players id

        Returns
        -------
            character: string - The current player's character
        """
        return "O" if player_index == 2 else "X"

    def possible_moves(self):
        """
        Returns an array of possible moves

        Returns
        -------
            moves: list - list of possible moves
        """
        return [c + 1 for c in range(self.__cols) if self.__board[0][c] == ""]

    def make_move(self, column: int):
        """
        A method to make a move during the game

        Parameters
        ----------
            column: int - Selected column to input character
        """

        row: int = max(
            [r for r in range(self.__rows) if self.__board[r][column - 1] == ""]
        )
        self.__board[row][column - 1] = self._get_current_player_character(
            self.current_player
        )

    def lose(self) -> bool:
        """
        Returns value from find_four method

        Returns
        -------
            value: bool - returned value from find_four method
        """
        return self._find_four()

    def is_over(self):
        """
        Returns bool value whether the game is over or not

        Returns
        -------
            value: bool - whether the game is over or not
        """
        return len(self.possible_moves()) == 0 or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0

    def show(self):
        """
        Shows the board after each move,
        and current possible moves
        """
        print(
            "\n".join(
                [
                    " ".join([str(x) for x in range(1, self.__cols + 2)]),
                    (2 * self.__cols + 1) * "-",
                ]
                + [
                    " ".join([col if len(col) else "." for col in row])
                    for row in self.__board
                ]
            ),
            "\n\n",
        )

        print(
            "Possible moves for current player: ",
            ", ".join(map(str, self.possible_moves())),
        )
