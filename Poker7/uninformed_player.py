from pypokerengine.players import BasePokerPlayer
from hand_type import handType

class UninformedPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        hand = hole_card + round_state['community_card']
        # print(hand, round_state['community_card'])
        type_of_hand = handType(hand)
        # print(hand, type_of_hand)
        threshold = type_of_hand*100
        # print(round_state['pot']['main']['amount'], threshold, hand, type_of_hand)
        for action in valid_actions:
            if round_state['pot']['main']['amount'] < threshold or (round_state['street'] == 'preflop' and type_of_hand == 2):
                if 'raise' == action['action']:
                    return 'raise'
        for action in valid_actions:
            if round_state['pot']['main']['amount'] <= threshold or (round_state['street'] == 'preflop' and type_of_hand == 1):
                if 'call' == action['action']:
                    return 'call'
        return 'fold'
    
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
    return UninformedPlayer()

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