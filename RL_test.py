from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from uninformed_player import UninformedPlayer
from RL_player import RLPlayer

#TODO:config the config as you wish
config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)

# config.register_player(name="rand", algorithm=RandomPlayer())
# config.register_player(name="raise", algorithm=RaisedPlayer())
config.register_player(name="unif", algorithm=UninformedPlayer())
config.register_player(name="RL", algorithm=RLPlayer())

game_result = start_poker(config, verbose=1)
