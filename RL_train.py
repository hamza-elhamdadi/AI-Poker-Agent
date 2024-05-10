from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from uninformed_player import UninformedPlayer
from RL_player import RLPlayer
from mcts_player import MCTSPlayer
from init_qtable import gen_table
import matplotlib.pyplot as plt

load = '|/-\\'
NUM_GAMES_PER_BATCH = 50
NUM_BATCHES = 50
opp = MCTSPlayer(gamma=0.7)
gen_table('qtable_trained.csv')
win_rates = []
config = setup_config(max_round=100, initial_stack=1000, small_blind_amount=10)
# config.register_player(name="rand", algorithm=RandomPlayer())
# config.register_player(name="raise", algorithm=RaisedPlayer())
config.register_player(name="mcts", algorithm=opp)
config.register_player(name="RL", algorithm=RLPlayer())
for batch in range(NUM_BATCHES):
    e_0 = 0.9
    d = 0.7
    wins = 0
    for game in range(NUM_GAMES_PER_BATCH):
        config.players_info[1]['algorithm'] = RLPlayer(epsilon=e_0 * d ** batch, isTraining=True)
        game_result = start_poker(config, verbose=0)
        sorted_stack = sorted(game_result['players'], key=lambda x: x['stack'], reverse=True)
        wins += int(sorted_stack[0]['name'] == 'RL')
        print(f'[{load[game % 4]}] EP: {batch+1: 3} GAME: {game+1: 3} WON: {wins/(game+1) * 100:.3f}%', end='\r')
    win_rate = wins / NUM_GAMES_PER_BATCH * 100
    win_rates.append(win_rate)
print()
plt.title('Win-rate of RL agent against MCTSPlayer')
plt.xlabel('batches')
plt.ylabel('percent of games won')
plt.plot(win_rates)
plt.savefig('RL_winrate_over_time_mcts.jpg')
