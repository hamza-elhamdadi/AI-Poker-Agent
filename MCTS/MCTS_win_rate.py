from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.engine.card import Card
import json
from tqdm import tqdm

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

def win_rate(hole_card, community_card = None, nb_simulation = 10000):
    num_community_cards = 0 if community_card == None else len(community_card)
    hole = map_cards_to_numbers(hole_card)
    community = map_cards_to_numbers(community_card)
    value = estimate_hole_card_win_rate(nb_simulation,2, hole, community)
    return value

all_cards = [suit + rank for suit in ['D', 'H', 'C', 'S'] for rank in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']]

preflop_map = {}

if __name__ == '__main__':
    for i in range(len(all_cards)):
        for j in tqdm(range(i+1,len(all_cards))):
            hole_cards = [all_cards[i], all_cards[j]]
            hole_cards.sort()
            preflop_map[''.join(hole_cards)] = win_rate(hole_cards,nb_simulation=1)
            # print(hole_cards)
            remaining_cards = all_cards.copy()
            remaining_cards.remove(all_cards[i])
            remaining_cards.remove(all_cards[j])

            flop_map = {}

            for k1 in range(len(remaining_cards)):
                for k2 in range(k1+1,len(remaining_cards)):
                    for k3 in range(k2+1,len(remaining_cards)):
                        community_cards = [remaining_cards[k1], remaining_cards[k2], remaining_cards[k3]]
                        community_cards.sort()
                        flop_map[''.join(community_cards)] = win_rate(hole_cards, community_cards, 1)
            with open(f'params/MCTS_params_flop_{"".join(hole_cards)}.json', 'w') as file:
                json.dump(flop_map, file)
                
    with open('params/MCTS_params_preflop.json', 'w') as file:
        json.dump(preflop_map, file)

    # print(len(all_cards))





