from pypokerengine.players import BasePokerPlayer

suits = ['C', 'S', 'D', 'H']

possible_cards = []
for suit in suits:
    for value in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']:
        possible_cards.append(suit + value)

valueMap = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

def checkFlush(values):
    pass

def checkStraight(start_idx, values):
    start_value = values[start_idx][1]
    isFlush = True
    for i in range(start_value+1, start_value+5):
        if not i in [v[1] for v in values]:
            isFlush = False
    return isFlush

def handType(hand):
    values = [(h[0], valueMap[h[1]]) for h in hand]
    values = sorted(values, key=lambda v: v[1])
    
    hasFlush = False
    for start_idx in [v[1] for v in values]:
        if checkFlush(start_idx, values):
            pass
        
    
    

class UninformedPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        hand = hole_card + round_state['community_card']
        print(hand)
        handType(hand)
        return valid_actions[1]['action']
    
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