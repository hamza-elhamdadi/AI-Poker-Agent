import sys

sys.path.insert(0, "./pypokerengine/api/")
import game

setup_config = game.setup_config
start_poker = game.start_poker
import time
from argparse import ArgumentParser
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


def testperf(agent_name1, agent_name2):

    # Init to play 500 games of 1000 rounds
    num_game = 200
    max_round = 1000
    initial_stack = 10000
    smallblind_amount = 20

    # Init pot of players
    agent1_pot = 0
    agent2_pot = 0

    # Setting configuration
    config = setup_config(
        max_round=max_round,
        initial_stack=initial_stack,
        small_blind_amount=smallblind_amount,
    )

    our_player = MCTSPlayer()
    opponent_player = MCTSPlayer()

    # Register players
    config.register_player(name=agent_name1, algorithm=our_player)
    config.register_player(name=agent_name2, algorithm=opponent_player)
    # config.register_player(name=agent_name1, algorithm=agent1())
    # config.register_player(name=agent_name2, algorithm=agent2())

    # Start playing num_game games
    for game in tqdm(range(1, num_game + 1)):
        game_result = start_poker(config, verbose=0)
        agent1_pot = agent1_pot + game_result["players"][0]["stack"]
        agent2_pot = agent2_pot + game_result["players"][1]["stack"]

    print(
        "\n After playing {} games of {} rounds, the results are: ".format(
            num_game, max_round
        )
    )
    # print("\n Agent 1's final pot: ", agent1_pot)
    print("\n " + agent_name1 + "'s final pot: ", agent1_pot)
    print("\n " + agent_name2 + "'s final pot: ", agent2_pot)

    # print("\n ", game_result)
    # print("\n Random player's final stack: ", game_result['players'][0]['stack'])
    # print("\n " + agent_name + "'s final stack: ", game_result['players'][1]['stack'])

    if agent1_pot < agent2_pot:
        print("\n Sorry! " + agent_name2 + " has won.")
    elif agent1_pot > agent2_pot:
        print("\n Congratulations! " + agent_name1 + " has won.")
        # print("\n Random Player has won!")
    else:
        print("\n It's a draw!")

    print("opponent", our_player.Nr, our_player.Nc)
    print("our", opponent_player.Nr, opponent_player.Nc)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        "-n1", "--agent_name1", help="Name of agent 1", default="Your agent", type=str
    )
    parser.add_argument(
        "-n2",
        "--agent_name2",
        help="Name of agent 2",
        default="Opponent agent",
        type=str,
    )
    args = parser.parse_args()
    return args.agent_name1, args.agent_name2


if __name__ == "__main__":
    name1, name2 = parse_arguments()
    start = time.time()
    testperf(name1, name2)
    end = time.time()

    print("\n Time taken to play: %.4f seconds" % (end - start))
