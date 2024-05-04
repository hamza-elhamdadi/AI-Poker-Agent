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

    def __init__(self):
        # the following counts apply to the opponent to track aggression
        self.raises = 0
        self.calls = 0
        self.folds = 0
        self.last_street = 'river'
        self.num_raise_rounds = 0
        self.raised_last_round = 0
        
        # last action taken by agent
        self.last_action = None
        
        self.VPIP = 0
        
    def declare_action(self, valid_actions, hole_card, round_state):
        this_street = round_state['street']
        hand = hole_card + round_state['community_card']
        type_of_hand = handType(hand)
        # 1 if BIG, 0 if SMALL
        player_turn = round_state['next_player']
        blindedness = player_turn == round_state['big_blind_pos']
        
        round_history = round_state['action_histories'][this_street]
        if not round_history:
            round_history = round_state['action_histories'][self.last_street]
        
        last_opp_action = round_history[-1]['action']
        for i in range(player_turn, len(round_history), 2):
            last_opp_action = round_history[i]['action']
        
        if last_opp_action == 'CALL':
            self.calls += 1
        elif last_opp_action == 'RAISE':
            self.raises += 1
        else:
            last_opp_action = 'START'
            if self.last_street != 'river' and self.last_action != 'fold':
                self.folds += 1
            # percentage of games where opp raises once
            self.num_raise_rounds += 1 if self.raised_last_round != self.raises else 0
            self.raised_last_round = self.raises
        
        # aggression factor
        AF = self.raises - self.folds
        AF /= self.calls if self.calls else 1 
        
        # percentage of games where opp raises
        VPIP = self.num_raise_rounds / round_state['round_count']
        
        # add state for currently winning/losing
        sorted_stack = sorted(round_state['seats'], key=lambda x: x['stack'], reverse=True)
        winning = sorted_stack[0]['uuid'] == self.uuid
        
        print(last_opp_action, AF, VPIP, winning)
        # this_action = random.choice(valid_actions)['action']
        self.last_street = this_street
        this_action = 'call'
        self.last_action = this_action
        return this_action
    
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