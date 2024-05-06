from pypokerengine.players import BasePokerPlayer
from hand_type import handType
import json

from MCTS.MCTS_win_rate import win_rate

class MCTSPlayer(BasePokerPlayer):

    def estimate_reward(self, action, hole_card, round_state):
        import random
        return random.random()
        # TODO:Use MCTS to build a reward table

    def declare_action(self, valid_actions, hole_card, round_state):
        if round_state['street'] == 'preflop':
            type_of_hand = handType(hole_card + round_state['community_card'])
            if type_of_hand == 2:
                return 'raise'
            else:
                return 'call'
        else:
            best_action = 'call'
            
            hole_card.sort()
            community_values = [c[1] for c in round_state['community_card']]
            community_values.sort()

            if round_state['street'] == 'flop':
                with open(f'MCTS/params/MCTS_params_flop_{"".join(hole_card)}.json', 'r') as file:
                    win_rates = json.load(file)
                win_rt = win_rates[''.join(community_values)]
            else:
                win_rt = win_rate(hole_card)

            if win_rt <= 0.2:
                best_action = 'fold'
            elif win_rt <= 0.8:
                best_action = 'call'
            else:
                best_action = 'raise'

            return best_action

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return MCTSPlayer()