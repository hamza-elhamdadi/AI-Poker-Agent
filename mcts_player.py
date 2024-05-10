from pypokerengine.players import BasePokerPlayer
from hand_type import handType
import json
import os
import time
import numpy as np

from MCTS.MCTS_win_rate import win_rate

def average_base_win_rate_for_turn(hole_card, community_card):
    win_rt = []
    community_values = [c[1] for c in community_card]
    # get the corresponding pre-trained dictionary for the current hole cards
    with open(f'MCTS/params/MCTS_params_flop_{"".join(hole_card)}.json', 'r') as file:
        win_rates = json.load(file)
    # get corresponding win rate for ranks of the
    # first three community cards
    win_rt.append(win_rates[''.join(np.sort(community_values[:-1]))])
    # last three community cards
    win_rt.append(win_rates[''.join(np.sort(community_values[1:]))])
    # first community card and last two community cards
    win_rt.append(win_rates[''.join(np.sort(community_values[:1]+community_values[2:]))])
    # first two community cards and last two community cards
    win_rt.append(win_rates[''.join(np.sort(community_values[:2]+community_values[3:]))])

    # adjust the hole cards to be the first hole card and the first community card
    adjusted_hole = hole_card[:1]+community_card[:1]
    adjusted_hole.sort()
    # get the corresponding pre-trained dictionary for the adjusted hole cards
    with open(f'MCTS/params/MCTS_params_flop_{"".join(adjusted_hole)}.json', 'r') as file:
        win_rates = json.load(file)
    win_rt.append(win_rates[''.join(np.sort(community_values[1:]))])

    # adjust the hole cards to be the second hole card and the first community card
    adjusted_hole = hole_card[1:]+community_card[:1]
    adjusted_hole.sort()
    # get the corresponding pre-trained dictionary for the adjusted hole cards
    with open(f'MCTS/params/MCTS_params_flop_{"".join(adjusted_hole)}.json', 'r') as file:
        win_rates = json.load(file)
    win_rt.append(win_rates[''.join(np.sort(community_values[1:]))])

    # return max(win_rt)
    return sum(win_rt)/len(win_rt)

def compute_raise_rate(self, action_histories, curr_street, opponent_uuid):
    nr, nc = 0, 0

    # set the streets we will check based on the current street
    if curr_street == 'preflop':
        streets = ['preflop']
    elif curr_street == 'flop':
        streets = ['preflop', 'flop']
    elif curr_street == 'turn':
        streets = ['preflop', 'flop', 'turn']
    else:
        streets = ['preflop', 'flop', 'turn', 'river']
    
    # get the number of times our opponent called and raised in this round
    for street in streets:
        for action in action_histories[street]:
            if action['action'] == 'CALL' and action['uuid'] == opponent_uuid:
                nc += 1
            if action['action'] == 'RAISE' and action['uuid'] == opponent_uuid:
                nr += 1

    # update the total number of times they called and raised over the entire game
    self.Nr += nr
    self.Nc += nc

    pb, pa2 = 0, 0
    # compute the percentage of raises in this round
    if nr + nc != 0:
        pb = nr/(nr+nc)
    # compute the percentage of raises in the entire game
    if self.Nr + self.Nc != 0:
        pa2 = self.Nr/(self.Nr+self.Nc)
    return pa2, pb

def get_street_num(street):
    return (street=='preflop') + (street=='flop')*2 + (street=='turn')*3 + (street=='river')*4

class MCTSPlayer(BasePokerPlayer):
    
    def __init__(self, gamma=0.7):
        self.Nc = 0
        self.Nr = 0
        self.gamma = gamma


    def declare_action(self, valid_actions, hole_card, round_state):
        opponent_uuid = ''
        # get the opponent's uuid
        for seat in round_state['seats']:
            if seat['uuid'] != self.uuid:
                opponent_uuid = seat['uuid']

        if round_state['street'] == 'preflop':
            type_of_hand = handType(hole_card + round_state['community_card'])

            # if the hole cards are a pair, raise, otherwise call
            if type_of_hand == 2:
                return 'raise'
            else:
                return 'call'
        else:
            hole_card.sort()
            community_values = [c[1] for c in round_state['community_card']]
            community_values.sort()

            if round_state['street'] == 'flop':
                # get pretrained dictionary for current hole cards
                with open(f'MCTS/params/MCTS_params_flop_{"".join(hole_card)}.json', 'r') as file:
                    win_rates = json.load(file)
                # get corresponding win rate for ranks of community cards
                pw = win_rates[''.join(community_values)]
                pa2, pb = compute_raise_rate(self, round_state['action_histories'], 'flop', opponent_uuid)
                
            elif round_state['street'] == 'turn':
                # compute the win rate based on all 6 combinations of 5 cards.
                pw = average_base_win_rate_for_turn(hole_card, round_state['community_card'])
                pa2, pb = compute_raise_rate(self, round_state['action_histories'], 'turn', opponent_uuid)

            else:
                # get the hand type
                type_of_hand = handType(hole_card + round_state['community_card'])
                # open the dictionary for hand type win rates in the river street
                with open(f'MCTS/params/MCTS_params_river.json', 'r') as file:
                    win_rates = json.load(file)
                # get the corresponding win rate for the hand type
                pw = win_rates[type_of_hand-1]
                pa2, pb = compute_raise_rate(self, round_state['action_histories'], 'river', opponent_uuid)
            
            # trained from MCTSPlayer vs MCTSPlayer
            pa1 = 0.44417431136246915

            # probability that the opponent will raise if they stay in the game
            pa = (pa1 + pa2)/2

            # cost of staying in the game
            c = 20 + self.gamma*pa*(4-get_street_num(round_state['street']))*20

            # amount at stake
            amt_at_stake = round_state['pot']['main']['amount'] + 2*c

            # winning threshold
            alpha = c/amt_at_stake

            # compute the probability that our opponent will win
            if pb <= pa:
                po = alpha + (0.5 - alpha)*pb/pa
            else:
                po = 0.5 + 0.5*(pb - pa)/(1 - pa)

            # compute the adjusted probability that we will win
            if po >= 0.5:
                p = pw - self.gamma*pw*(po - 0.5)/0.5
            else:
                p = pw + self.gamma*(1-pw)*(0.5 - po)/0.5
            
            # compute the expected return
            b = p*amt_at_stake

            # if the expected return is less than the cost of staying the game, then fold
            if b < c:
                return 'fold'
            # otherwise raise with probability p and call with probability 1-p
            else:
                return np.random.choice(['raise', 'call'], p=[p,1-p])

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