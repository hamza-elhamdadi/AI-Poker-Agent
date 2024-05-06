from pypokerengine.players import BasePokerPlayer
from hand_type import handType
import json
import time

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
            elif round_state['street'] == 'turn':
                win_rt = []
                with open(f'MCTS/params/MCTS_params_flop_{"".join(hole_card)}.json', 'r') as file:
                    win_rates = json.load(file)
                win_rt.append(win_rates[''.join(community_values[:-1])])
                win_rt.append(win_rates[''.join(community_values[1:])])
                win_rt.append(win_rates[''.join(community_values[:1]+community_values[2:])])
                win_rt.append(win_rates[''.join(community_values[:2]+community_values[3:])])

                adjusted_hole = hole_card[:1]+round_state["community_card"][:1]
                adjusted_hole.sort()
                with open(f'MCTS/params/MCTS_params_flop_{"".join(adjusted_hole)}.json', 'r') as file:
                    win_rates = json.load(file)
                win_rt.append(win_rates[''.join(community_values[1:])])

                adjusted_hole = hole_card[1:]+round_state["community_card"][:1]
                adjusted_hole.sort()
                with open(f'MCTS/params/MCTS_params_flop_{"".join(adjusted_hole)}.json', 'r') as file:
                    win_rates = json.load(file)
                win_rt.append(win_rates[''.join(community_values[1:])])
                win_rt = sum(win_rt)/len(win_rt)
            else:
                win_rt = win_rate(hole_card)

            if win_rt <= 0.2:
                best_action = 'fold'
            elif win_rt <= 0.66:
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