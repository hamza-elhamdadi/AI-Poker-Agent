from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from uninformed_player import UninformedPlayer
from RL_player import RLPlayer
from Group7Player import Group7Player
from init_qtable import gen_table
import matplotlib.pyplot as plt

load = '|/-\\'
NUM_GAMES = 100
# opp = Group7Player(gamma=0.7)
def play(trained_name, opp_name, opp):
    # gen_table('qtable_trained.csv')
    win_rates = []
    config = setup_config(max_round=100, initial_stack=1000, small_blind_amount=10)
    # config.register_player(name="rand", algorithm=RandomPlayer())
    # config.register_player(name="raise", algorithm=RaisedPlayer())
    config.register_player(name=opp_name, algorithm=opp)
    config.register_player(name="RL", algorithm=RLPlayer())
    wins = 0
    for game in range(NUM_GAMES):
        config.players_info[1]['algorithm'] = RLPlayer(isTraining=False, inFile=f'qtable_vs_{trained_name}.csv')
        game_result = start_poker(config, verbose=0)
        sorted_stack = sorted(game_result['players'], key=lambda x: x['stack'], reverse=True)
        wins += int(sorted_stack[0]['name'] == 'RL')
        print(f'[{load[game % 4]}] VS: {opp_name} GAME: {game+1: 3} WON: {wins/(game+1) * 100:.3f}%', end='\r')
    win_rate = wins / NUM_GAMES * 100
    print()

agents = {'uninformed': UninformedPlayer(), 'raised': RaisedPlayer(), 'mcts': Group7Player(gamma=0.7)}
for trained_on_name in agents:
    for opp_name in agents:
        print(f'Trained on {trained_on_name} against {opp_name}')
        play(trained_on_name, opp_name, agents[opp_name])
