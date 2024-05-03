from pypokerengine.players import BasePokerPlayer
import json

from MCTS.MCTS_win_rate import win_rate

class MCTSPlayer(BasePokerPlayer):

    def estimate_reward(self, action, hole_card, round_state):
        import random
        return random.random()
        # TODO:Use MCTS to build a reward table

    def declare_action(self, valid_actions, hole_card, round_state):
        best_action = 'call'
        print(hole_card)
        
        hole_card.sort()
        community_card = round_state['community_card']
        community_card.sort()

        if round_state['street'] == 'preflop':
            with open('MCTS/params/MCTS_params_preflop.json', 'r') as file:
                win_rates = json.load(file)
            
            win_rt = win_rates[''.join(hole_card)]
        elif round_state['street'] == 'flop':
            with open(f'MCTS/params/MCTS_params_flop_{"".join(hole_card)}.json', 'r') as file:
                win_rates = json.load(file)
            win_rt = win_rates[''.join(community_card)]
        else:
            win_rt = win_rate(hole_card)

        print(win_rt)

        for i in valid_actions:
            action = i['action']
            #reward = self.estimate_reward(action, hole_card, round_state)
            if action == 'fold':
                if win_rt <= 0.2:
                    best_action = action
            if action == 'call':
                if 0.2 < win_rt <= 0.8:
                    best_action = action
            if action == 'raise':
                if win_rt > 0.8:
                    best_action = action
                    
            #if reward > highest_reward:
                #highest_reward = reward
            #best_action = action

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