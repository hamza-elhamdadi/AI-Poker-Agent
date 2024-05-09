import time
from MCTS_win_rate import map_cards_to_numbers, win_rate
from pypokerengine.utils.card_utils import evaluate_hand
from tqdm import tqdm
import json



def river_win_rate(hole_card, community_card):
    start_time = time.time()
    deck = [suit + rank for suit in ['D', 'H', 'C', 'S'] for rank in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']]
    for card in hole_card:
        deck.remove(card)
    for card in community_card:
        deck.remove(card)
    deck = map_cards_to_numbers(deck)
    hole_card = map_cards_to_numbers(hole_card)
    community_card = map_cards_to_numbers(community_card)
    hand_strength = evaluate_hand(hole_card, community_card)['strength']

    nw, nl = 0, 0

    for i in range(len(deck)):
        A = deck[i]
        for j in range(i+1, len(deck)):
            B = deck[j]
            opponent_hole = [A, B]
            opponent_strength = evaluate_hand(opponent_hole, community_card)['strength']
            if opponent_strength > hand_strength:
                nl += 1
            if opponent_strength < hand_strength:
                nw += 1
            if opponent_strength == hand_strength:
                nl += 0.5
                nw += 0.5

    win_rate = nw/(nw + nl)
    print(win_rate)
    print(nw)
    print(nl)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Time elapsed:", elapsed_time, "seconds")


def river_win_rate_by_hand_type():
    hands_low = [
        ['HT', 'HJ', 'HQ', 'HK', 'HA', 'S2', 'S3'],
        ['H2', 'H3', 'H4', 'H5', 'H6', 'S8', 'S9'],
        ['H2', 'S2', 'D2', 'C2', 'S4', 'S7', 'S3'],
        ['H2', 'S2', 'D2', 'H3', 'D3', 'S7', 'S4'],
        ['H2', 'H3', 'H4', 'H5', 'H7', 'S8', 'ST'],
        ['H2', 'S3', 'H4', 'S5', 'H6', 'SJ', 'SQ'],
        ['H2', 'S2', 'D2', 'C5', 'C8', 'HT', 'CJ'],
        ['H2', 'S2', 'H3', 'S3', 'C5', 'C7', 'H9'],
        ['H2', 'S2', 'CT', 'C9', 'H7', 'D5', 'DQ'],
        ['H2', 'H3', 'H4', 'H5', 'D7', 'D8', 'D9']
    ]

    hands_high = [
        ['HT', 'HJ', 'HQ', 'HK', 'HA', 'S2', 'S3'],
        ['H9', 'HT', 'HJ', 'HQ', 'HK', 'S2', 'S3'],
        ['HA', 'SA', 'DA', 'CA', 'S4', 'S2', 'S3'],
        ['HA', 'SA', 'DA', 'HK', 'DK', 'S2', 'S3'],
        ['H9', 'HJ', 'HQ', 'HK', 'HA', 'S2', 'S3'],
        ['HT', 'SJ', 'HQ', 'SK', 'HA', 'S2', 'S3'],
        ['HA', 'SA', 'DA', 'C2', 'C3', 'H4', 'C6'],
        ['HA', 'SA', 'HK', 'SK', 'C2', 'C3', 'H4'],
        ['HA', 'SA', 'C2', 'C3', 'H4', 'D8', 'D9'],
        ['HA', 'C2', 'C3', 'H4', 'D8', 'D9', 'DJ']
    ]
    
    win_rates = []
    for i in tqdm(range(len(hands_low))):
        low_win_rt = win_rate(hands_low[i][:2], hands_low[i][2:], int(1e5))
        high_win_rt = win_rate(hands_high[i][:2], hands_high[i][2:], int(1e5))
        win_rates.append((low_win_rt+high_win_rt)/2)
    

    print(win_rates)
    print(list(reversed(win_rates)))
    with open('params/MCTS_params_river.json', 'w') as file:
        json.dump(list(reversed(win_rates)), file)






if __name__ == '__main__':
    river_win_rate_by_hand_type()