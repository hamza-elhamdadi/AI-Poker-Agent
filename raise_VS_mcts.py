from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from MCTS.mcts_player import MCTSPlayer
from MCTS.expplayer import EXPPlayer

#TODO:config the config as our wish
config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)



config.register_player(name="f1", algorithm=MCTSPlayer())
config.register_player(name="FT2", algorithm=RandomPlayer())


game_result = start_poker(config, verbose=1)