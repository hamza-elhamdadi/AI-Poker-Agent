from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.engine.card import Card

import time

def map_cards_to_numbers(card_list):
    SUIT_MAP = {
        'C': 2,
        'D': 4,
        'H': 8,
        'S': 16
    }

    RANK_MAP = {
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

    cards = []
    if card_list != None:
        for card in card_list:
            suit = card[0]  # First character is the suit
            rank = card[1]  # Second character is the rank
            mapped_suit = SUIT_MAP[suit]
            mapped_rank = RANK_MAP[rank]
            mapped_card = Card(mapped_suit, mapped_rank)
            cards.append(mapped_card)
    return cards

def win_rate(hole_card, community_card = None):
    num_community_cards = 0 if community_card == None else len(community_card)
    hole = map_cards_to_numbers(hole_card)
    community = map_cards_to_numbers(community_card)
    value = estimate_hole_card_win_rate(1000 if num_community_cards < 4 else int(7e6),2, hole, community)
    return value

#example
# start_time = time.time()
#
# hole_card = [Card(2, 14), Card(4, 14)]
# community_card = [Card(8, 14), Card(16, 14), Card(16, 11)]
# #value = estimate_hole_card_win_rate(300,2,hole_card, community_card)
#
# value = win_rate(hole_card, community_card)
#
# print(value)
#
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time} seconds")


