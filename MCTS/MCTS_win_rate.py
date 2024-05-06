from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.engine.card import Card
import json
from tqdm import tqdm
import numpy as np

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

count_nb = 0

all_cards = [suit + rank for suit in ['D', 'H', 'C', 'S'] for rank in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']]
nb_sims = 1000
if __name__ == '__main__':
    for i in range(len(all_cards)):
        for j in tqdm(range(i+1,len(all_cards))):
            hole_cards = [all_cards[i], all_cards[j]]
            hole_cards.sort()

            remaining_cards = all_cards.copy()
            remaining_cards.remove(all_cards[i])
            remaining_cards.remove(all_cards[j])
            remaining_cards = np.random.permutation(remaining_cards)

            flop_map = {}

            for k1 in range(len(remaining_cards)):
                for k2 in range(k1+1,len(remaining_cards)):
                    for k3 in range(k2+1,len(remaining_cards)):
                        community_cards = [remaining_cards[k1], remaining_cards[k2], remaining_cards[k3]]
                        community_values = [c[1] for c in community_cards]
                        community_values.sort()
                        if not ''.join(community_values) in flop_map:
                            flop_map[''.join(community_values)] = win_rate(hole_cards, community_cards, nb_sims)
            with open(f'MCTS/params/MCTS_params_flop_{"".join(hole_cards)}.json', 'w') as file:
                json.dump(flop_map, file)
                
print(count_nb)




