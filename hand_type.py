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

def checkStraightFromValue(start_value, values):
    is_flush = True
    for i in range(start_value+1, start_value+5):
        if not i in values:
            is_flush = False
    return is_flush

def checkStraight(values):
    for start_idx in range(3):
        start_value = values[start_idx]
        if checkStraightFromValue(start_value, values):
            return True
    return False

def handType(hand):
    cards = [(h[0], valueMap[h[1]]) for h in hand]
    cards = sorted(cards, key=lambda v: v[1])
    card_suits = [v[0] for v in cards]
    values = [v[1] for v in cards]

    #print(cards)
    
    if checkFlush(card_suits) and checkStraightFromValue(10, values) and 10 in values:
        print('has a royal flush')
        return ROYAL_FLUSH
        
    if checkFlush(card_suits) and checkStraight(values):
        print('has a straight flush')
        return STRAIGHT_FLUSH

    if checkStraight(values):
        print('has a straight')
        return STRAIGHT

    if checkFlush(card_suits):
        print('has a flush')
        return FLUSH

    return checkMatching(values)

def handType_2cards(hand):
    cards = [(h[0], valueMap[h[1]]) for h in hand]
    cards = sorted(cards, key=lambda v: v[1])
    card_suits = [v[0] for v in cards]
    values = [v[1] for v in cards]
    if values[0]==values[1]:
        return 2
    diff = values[1]-values[0]
    same_suits = card_suits[0]==card_suits[1]
    if diff > 0 and diff < 5:
        if same_suits:
            return 5
        return 3
    if same_suits:
        return 4
    return 1