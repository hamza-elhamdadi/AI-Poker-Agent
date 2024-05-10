from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from mcts_player import MCTSPlayer
from uninformed_player import UninformedPlayer

#TODO:config the config as you wish
config = setup_config(max_round=200, initial_stack=1000, small_blind_amount=10)



config.register_player(name="f1", algorithm=MCTSPlayer())
config.register_player(name="FT2", algorithm=RaisedPlayer())


game_result = start_poker(config)
