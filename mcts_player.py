from pypokerengine.players import BasePokerPlayer
from hand_type import handType
import json
import os
import time

from MCTS.MCTS_win_rate import win_rate

def average_base_win_rate(hole_card, community_card, community_values):
    win_rt = []
    with open(f'MCTS/params/MCTS_params_flop_{"".join(hole_card)}.json', 'r') as file:
        win_rates = json.load(file)
    win_rt.append(win_rates[''.join(community_values[:-1])])
    win_rt.append(win_rates[''.join(community_values[1:])])
    win_rt.append(win_rates[''.join(community_values[:1]+community_values[2:])])
    win_rt.append(win_rates[''.join(community_values[:2]+community_values[3:])])

    adjusted_hole = hole_card[:1]+community_card[:1]
    adjusted_hole.sort()
    with open(f'MCTS/params/MCTS_params_flop_{"".join(adjusted_hole)}.json', 'r') as file:
        win_rates = json.load(file)
    win_rt.append(win_rates[''.join(community_values[1:])])

    adjusted_hole = hole_card[1:]+community_card[:1]
    adjusted_hole.sort()
    with open(f'MCTS/params/MCTS_params_flop_{"".join(adjusted_hole)}.json', 'r') as file:
        win_rates = json.load(file)
    win_rt.append(win_rates[''.join(community_values[1:])])

    # return max(win_rt)
    return sum(win_rt)/len(win_rt)

def compute_raise_rate(action_histories, curr_street, opponent_uuid):
    nr, nc = 0, 0

    if curr_street == 'preflop':
        streets = ['preflop']
    elif curr_street == 'flop':
        streets = ['preflop', 'flop']
    elif curr_street == 'turn':
        streets = ['preflop', 'flop', 'turn']
    else:
        streets = ['preflop', 'flop', 'turn', 'river']
    
    for street in streets:
        for action in action_histories[street]:
            if action['action'] == 'CALL' and action['uuid'] == opponent_uuid:
                nc += 1
            if action['action'] == 'RAISE' and action['uuid'] == opponent_uuid:
                nr += 1


    if os.path.exists(f'MCTS/opponent_data/{opponent_uuid}.txt'):
        with open(f'MCTS/opponent_data/{opponent_uuid}.txt', 'r') as file:
            line = file.read()
            Nr, Nc = [int(x) for x in line.split(',')]
    else:
        Nr, Nc = 0,0

    Nr += nr
    Nc += nc

    with open(f'MCTS/opponent_data/{opponent_uuid}.txt', 'w') as file:
        file.write(f'{Nr},{Nc}')

    pb, pa2 = 0, 0
    if nr + nc != 0:
        pb = nr/(nr+nc)
    if Nr + Nc != 0:
        pa2 = Nr/(Nr+Nc)
    return pa2, pb

def get_street_num(street):
    return (street=='preflop') + (street=='flop')*2 + (street=='turn')*3 + (street=='river')*4

class MCTSPlayer(BasePokerPlayer):

    def estimate_reward(self, action, hole_card, round_state):
        import random
        return random.random()
        # TODO:Use MCTS to build a reward table

    def declare_action(self, valid_actions, hole_card, round_state):
        # print(round_state['action_histories'])
        print(round_state['seats'])
        # print(self.uuid)
        opponent_uuid = ''
        for seat in round_state['seats']:
            if seat['uuid'] != self.uuid:
                opponent_uuid = seat['uuid']

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
                pw = win_rates[''.join(community_values)]
                pa2, pb = compute_raise_rate(round_state['action_histories'], 'flop', opponent_uuid)
                
                
            elif round_state['street'] == 'turn':
                pw = average_base_win_rate(hole_card, round_state['community_card'], community_values)
                pa2, pb = compute_raise_rate(round_state['action_histories'], 'turn', opponent_uuid)


            else:
                pw = win_rate(hole_card)
                pa2, pb = compute_raise_rate(round_state['action_histories'], 'river', opponent_uuid)

            alpha = 0.3
            gamma = 0.5

            pa1 = 0.3
            # pa2 = pb

            pa = (pa1 + pa2)/2
            print('pb:', pb)

            if pb <= pa:
                po = alpha + (0.5 - alpha)*pb/pa
            else:
                po = 0.5 + 0.5*(pb - pa)/(1 - pa)

            if po >= 0.5:
                p = pw - gamma*pw*(po - 0.5)/0.5
            else:
                p = pw + gamma*(1-pw)*(0.5 - po)/0.5
            
            c = 20 + gamma*pa*(4-get_street_num(round_state['street']))*20
            
            b = p*(round_state['pot']['main']['amount'] + 2*c)

            if b < c:
                return 'fold'
            else:
                return 'raise' if p > 0.8 else 'call'

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