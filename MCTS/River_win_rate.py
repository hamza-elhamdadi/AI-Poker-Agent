import time
from hand_type import handType
from MCTS_win_rate import map_cards_to_numbers
from pypokerengine.utils.card_utils import evaluate_hand

start_time = time.time()

card_list = map_cards_to_numbers([suit + rank for suit in ['D', 'H', 'C', 'S'] for rank in [
    '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']])
my_hole = card_list[15:17]
community = card_list[17:22]
my_card = my_hole + community
my_strength = evaluate_hand(my_hole, community)['strength']

remaining_cards = card_list
del remaining_cards[15:22]

nw = 0
nl = 0

for i in range(45):
    A = remaining_cards[i]
    for j in range(i+1, 45):
        B = remaining_cards[j]
        opponent_hole = [A, B]
        opponent_strength = evaluate_hand(opponent_hole, community)['strength']
        if opponent_strength > my_strength:
            nl += 1
        if opponent_strength < my_strength:
            nw += 1

win_rate = nw/(nw + nl)
print(win_rate)
print(nw)
print(nl)

end_time = time.time()

elapsed_time = end_time - start_time
print("Time elapsed:", elapsed_time, "seconds")
