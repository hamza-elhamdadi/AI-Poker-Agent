import sys
sys.path.insert(0, './pypokerengine/api/')
import game
setup_config = game.setup_config
start_poker = game.start_poker
from tabulate import tabulate
from tqdm import tqdm


""" =========== *Remember to import your agent!!! =========== """
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from mcts_player import MCTSPlayer
# from smartwarrior import SmartWarrior
""" ========================================================= """

""" Example---To run testperf.py with random warrior AI against itself. 

$ python testperf.py -n1 "Random Warrior 1" -a1 RandomPlayer -n2 "Random Warrior 2" -a2 RandomPlayer
"""

def testhyperparam(agent_name1, agent_name2, gamma1, gamma2):		
    
    # Init to play 500 games of 1000 rounds
    num_game = 200
    max_round = 1000
    initial_stack = 10000
    smallblind_amount = 20

    # Init pot of players
    agent1_pot = 0
    agent2_pot = 0

    # Setting configuration
    config = setup_config(max_round=max_round, initial_stack=initial_stack, small_blind_amount=smallblind_amount)

    our_player = MCTSPlayer(gamma=gamma1)
    opponent_player = MCTSPlayer(gamma=gamma2)

    # Register players
    config.register_player(name=agent_name1, algorithm=our_player)
    config.register_player(name=agent_name2, algorithm=opponent_player)
    # config.register_player(name=agent_name1, algorithm=agent1())
    # config.register_player(name=agent_name2, algorithm=agent2())


    # Start playing num_game games
    for game in tqdm(range(1, num_game+1)):
        game_result = start_poker(config, verbose=0)
        agent1_pot = agent1_pot + game_result['players'][0]['stack']
        agent2_pot = agent2_pot + game_result['players'][1]['stack']

    # print("\n After playing {} games of {} rounds, the results are: ".format(num_game, max_round))
    # # print("\n Agent 1's final pot: ", agent1_pot)
    # print("\n " + agent_name1 + "'s final pot: ", agent1_pot)
    # print("\n " + agent_name2 + "'s final pot: ", agent2_pot)

    # print("\n ", game_result)
    # print("\n Random player's final stack: ", game_result['players'][0]['stack'])
    # print("\n " + agent_name + "'s final stack: ", game_result['players'][1]['stack'])

    # if (agent1_pot<agent2_pot):
    #     print("\n Sorry! " + agent_name2 + " has won.")
    # elif(agent1_pot>agent2_pot):
    #     print("\n Congratulations! " + agent_name1 + " has won.")
    #     # print("\n Random Player has won!")
    # else:
    #     print("\n It's a draw!") 
	
    return agent2_pot - agent1_pot, our_player.Nr, our_player.Nc

if __name__ == '__main__':
    table = []
    head = ['gamma1', 'gamma2', 'loss', 'number of opponent raises', 'number of opponent calls']
    gammas = [0.2, 0.3, 0.5, 0.6, 0.7]
    for g1 in range(len(gammas)):
        for g2 in range(g1+1,len(gammas)):
            loss, Nr, Nc = testhyperparam('MCTS', 'Raised', gammas[g1], gammas[g2])
            table.append([gammas[g1], gammas[g2], loss, Nr, Nc])
        
    print(tabulate(table, headers=head, tablefmt='latex_raw'))