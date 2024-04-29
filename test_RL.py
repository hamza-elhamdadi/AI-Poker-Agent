from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from uninformed_player import UninformedPlayer
from RL_player import RLPlayer


def main():
    config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)

    config.register_player(name="RL_Player", algorithm=RLPlayer())
    config.register_player(name="Rand_Player", algorithm=RandomPlayer())
    # config.register_player(name="Raised_Player", algorithm=RaisedPlayer())

    game_result = start_poker(config, verbose=1)


if __name__ == '__main__':
    main()
