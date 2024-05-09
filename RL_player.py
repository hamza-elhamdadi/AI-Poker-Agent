# Jay's agent using SARSA TD-learning algorithm
"""
DONE:
    - Gather full intel on state at each round
    - Generate/Init Q-table
    - Use state info to index Q-table
    - Write SARSA update function
TODO:
    - Implement epsilon-greedy for training
    - Train against various agents
"""

from pypokerengine.players import BasePokerPlayer
from hand_type import handType
import pandas as pd
import random

pd.options.mode.chained_assignment = None

class RLPlayer(BasePokerPlayer):

    def __init__(self, epsilon=0):
        # action counts / for tracking player states
        self.raises = 0
        self.calls = 0
        self.folds = 0
        self.last_street = 'river'
        self.num_raise_rounds = 0
        self.raised_last_round = 0
        self.last_round_keys = []
        self.starting_pot = 1000
        self.last_pot = 0
        self.input_fname = 'RL_models/qtable_trained.csv'
        self.output_fname = 'RL_models/qtable_trained.csv'
        self.qtable = pd.read_csv(self.input_fname)
        self.last_q_value = 0
        
        # hyperparams
        self.AF_THRESH = 25
        self.VPIP_THRESH = 0.6
        self.alpha = 0.5  # learning rate in [0, 1]
        self.gamma = 0.5  # discount rate in [0, 1]
        self.epsilon = epsilon  # for epsilon-greedy training
        
        self.isTraining = True
    
    def declare_action(self, valid_actions, hole_card, round_state):
        r = random.random()
        this_street = round_state['street']
        street_num = ['preflop', 'flop', 'turn', 'river'].index(this_street)
        hand = hole_card + round_state['community_card']
        hand_rank = handType(hand) - 1
        
        # 1 if BIG, 0 if SMALL
        player_turn = round_state['next_player']
        blindedness = int(player_turn == round_state['big_blind_pos'])
    
        # add state for currently winning/losing
        sorted_stack = sorted(round_state['seats'], key=lambda x: x['stack'], reverse=True)
        winning = int(sorted_stack[0]['uuid'] == self.uuid)
        my_pot = sorted_stack[(winning + 1) % 2]['stack']
        
        round_history = round_state['action_histories'][this_street]
        
        # if beginning of round
        if this_street == 'preflop' and len(round_history) <= 3:
            this_starting_pot = my_pot + (20 if blindedness else 10)
            reward = this_starting_pot - self.starting_pot
            # if reward >= 0:
            #     print('\tWON', reward)
            # else:
            #     print('\tLOST', reward)

            # update qtable
            if self.isTraining:
                Q_tplus1 = reward
                for state_key, action_idx in reversed(self.last_round_keys):
                    Q_t = self.qtable[state_key][action_idx]
                    self.qtable[state_key][action_idx] += self.alpha * ((self.gamma * Q_tplus1) - Q_t)
                    Q_tplus1 = Q_t
                self.qtable.to_csv(self.output_fname, index=None)

            # get opponent number of folds
            if self.last_street != 'river' and self.last_round_keys[-1][1] != 0:
                self.folds += 1

            self.starting_pot = this_starting_pot
            self.last_round_keys = []
        
        # get last opponent action / update action counts
        if not round_history:
            round_history = round_state['action_histories'][self.last_street]
        last_opp_action = round_history[-1]['action']
        for i in range(player_turn, len(round_history), 2):
            last_opp_action = round_history[i]['action']
        if last_opp_action == 'CALL':
            self.calls += 1
        elif last_opp_action == 'RAISE':
            self.raises += 1
        else:  # very start of round
            last_opp_action = 'CALL'
            self.num_raise_rounds += 1 if self.raised_last_round != self.raises else 0
            self.raised_last_round = self.raises
        
        # aggression factor
        AF = self.raises - self.folds
        AF /= self.calls if self.calls else 1
        
        # percentage of games where opp raises
        VPIP = self.num_raise_rounds / round_state['round_count']
        
        # generate key for indexing Q-table
        key = f'H{hand_rank}S{street_num}B{blindedness}L{int(last_opp_action == "RAISE")}'
        key += f'A{int(AF < self.AF_THRESH)}V{int(VPIP < self.VPIP_THRESH)}W{winning}'
        action_rewards = self.qtable[key]
        max_action_idx = action_rewards.idxmax()
        try:
            # epsilon-greedy action selection
            if random.random() > self.epsilon:
                this_action = valid_actions[max_action_idx]['action']
            else:
                this_action = random.choice(valid_actions)['action']
        except IndexError:
            this_action = 'call'
            
        self.last_street = this_street
        self.last_round_keys.append((key, max_action_idx))
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
