from easyAI import AI_Player, Human_Player, Negamax, SSS
from classes.game import Game


class CreateGame:
    def __int__(self):
        self.__player_1 = None
        self.__player_2 = None

    def _set_bot_level(self):
        """
        Return selected bot level

        Returns
        -------
        bot_level: int - Selected bot level
        """
        bot_level = int(input("Input level of bot's level: "))
        while bot_level < 1 or bot_level > 7:
            bot_level = int(input("Input level of bot's level: "))
        return bot_level

    def _create_opponent(self):
        """
        Creates an opponent for the player
        """
        bot_level = self._set_bot_level()
        bot_type = ""
        while bot_type not in ["sss", "neg"]:
            bot_type = input("Select bot type, 'sss' or 'neg': ")
            if bot_type == "sss":
                sss_ai = SSS(bot_level)
                self.__player_2 = AI_Player(sss_ai)
            elif bot_type == "neg":
                neg_ai = Negamax(bot_level)
                self.__player_2 = AI_Player(neg_ai)

    def _setup_game(self):
        """
        Creates the game configuration
        """
        player_choice = ""
        while player_choice == "" or player_choice not in ["player", "ai"]:
            player_choice = input(
                "Please select game type, 'player' to play against AI, or 'ai' to watch game between two AIs: "
            )

        if player_choice == "player":
            self.__player_1 = Human_Player()
            self._create_opponent()
        elif player_choice == "ai":
            bot_level = self._set_bot_level()
            neg_ai = Negamax(bot_level)
            sss_ai = SSS(bot_level)
            self.__player_1 = AI_Player(neg_ai)
            self.__player_2 = AI_Player(sss_ai)

    def start_game(self):
        """
        Creates the game configuration and launches it
        """
        self._setup_game()
        if self.__player_1 and self.__player_2:
            game = Game([self.__player_1, self.__player_2])
            game.play()
            if game.lose():
                print("Player %d wins." % (game.opponent_index))
            else:
                print("Looks like we have a draw.")
