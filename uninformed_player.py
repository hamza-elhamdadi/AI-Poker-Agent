from pypokerengine.players import BasePokerPlayer
import numpy as np

HIGHCARD = 1
PAIR = 2
TWO_PAIRS = 3
THREE_OF_A_KIND = 4
STRAIGHT = 5
FLUSH = 6
FULL_HOUSE = 7
FOUR_OF_A_KIND = 8
STRAIGHT_FLUSH = 9
ROYAL_FLUSH = 10

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

def checkMatching(values):
    vals, counts = np.unique(values, return_counts=True)
    counts = np.sort(counts)[::-1]
    if counts[0] == 4:
        print('has four of a kind')
        return FOUR_OF_A_KIND

    if counts[0] == 3:
        if len(counts) > 1 and counts[1] == 2:
            print('has a full house')
            return FULL_HOUSE
        print('has three of a kind')
        return THREE_OF_A_KIND

    if counts[0] == 2:
        if len(counts) > 1 and counts[1] == 2:
            print('has two pairs')
            return TWO_PAIRS
        print('has a pair')
        return PAIR
    
    print(f'has high card: {np.max(vals)}')
    return HIGHCARD


def checkFlush(card_suits):
    _, counts = np.unique(card_suits, return_counts=True)
    counts = np.sort(counts)[::-1]
    return counts[0] == 5

def checkStraight(values):
    for start_idx in range(3):
        start_value = values[start_idx]
        is_flush = True
        for i in range(start_value+1, start_value+5):
            if not i in values:
                is_flush = False
        if is_flush:
            return True
    return False

def handType(hand):
    cards = [(h[0], valueMap[h[1]]) for h in hand]
    cards = sorted(cards, key=lambda v: v[1])
    card_suits = [v[0] for v in cards]
    values = [v[1] for v in cards]

    print(cards)
    
    if checkFlush(card_suits) and checkStraight(values):
        if 10 in values[:3]:                    #TODO: NEEDS DEBUGGING
            print('has a royal flush')
            return ROYAL_FLUSH
        print('has a straight flush')
        return STRAIGHT_FLUSH

    if checkStraight(values):
        print('has a straight')
        return STRAIGHT

    if checkFlush(card_suits):
        print('has a flush')
        return FLUSH

    return checkMatching(values)
    
    

class UninformedPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        hand = hole_card + round_state['community_card']
        print(hand)
        type_of_hand = handType(hand)
        threshold = type_of_hand*10
        if round_state['pot'] < threshold:
            desired_action = 'call'
        for action in valid_actions:
            if desired_action == action['action']:
                return desired_action
        # TODO: ADD FUNCTIONALITY FOR RAISING TO THRESHOLD (OTHERWISE FOLD OR CALL? NOT SURE EXACTLY)
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