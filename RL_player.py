# Jay's agent using Q-learning
"""
TODO:
    - Gather full intel on state at each round
    - Generate/Init Q-table
    - Use state info to index Q-table
    - Write Q-learning update function
"""

from pypokerengine.players import BasePokerPlayer
from hand_type import handType
import random

class RLPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        hand = hole_card + round_state['community_card']
        type_of_hand = handType(hand)
        # 1 if BIG, 0 if SMALL
        blindedness = round_state['next_player'] == round_state['big_blind_pos']
        
        # TODO: get measures of aggressiveness
        
        last_action = list(round_state['action_histories'].values())[0][-1]['action']
        last_action = 'START' if last_action in ['BIGBLIND', 'SMALLBLIND'] else last_action
        print(last_action)
        return 'raise'
    
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
    return RLPlayer()

if __name__ == '__main__':
    hands = [
        ['C7', 'S7', 'H7', 'D4', 'CK'],
        ['C3', 'C4', 'H5', 'H6', 'D7'],
        ['C7', 'S7', 'H7', 'D7', 'CK'],
        ['C7', 'S7', 'H7', 'HK', 'CK'],
        ['HJ', 'HQ', 'HK', 'HA', 'HT']
    ]

    for hand in hands:
        print(f'hand value: {handType(hand)}')