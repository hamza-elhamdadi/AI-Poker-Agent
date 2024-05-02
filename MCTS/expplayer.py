from pypokerengine.players import BasePokerPlayer

#from MCTS.MCTS_win_rate import win_rate

class EXPPlayer(BasePokerPlayer):

    def estimate_reward(self, action, hole_card, round_state):
        import random
        return random.random()
        # TODO:Use MCTS to build a reward table

    def declare_action(self, valid_actions, hole_card, round_state):
        best_action = 'call'


        hole = hole_card
        card1 = hole[0]
        rank1 = card1[0]


        print(rank1)

        return best_action

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
    return MCTSPlayer()