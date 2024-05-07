import time
from MCTS_win_rate import map_cards_to_numbers
from pypokerengine.utils.card_utils import evaluate_hand



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

if __name__ == '__main__':
    river_win_rate(['DK', 'DQ'], ['DA', 'DJ', 'DT', 'S3', 'S2'])