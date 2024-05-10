from hand_type import handType

from pypokerengine.players import BasePokerPlayer

class RegretMinPlayer(BasePokerPlayer):

  def declare_action(self, valid_actions, hole_card, round_state):
    handtype = handType(hole_card + round_state['community_card'])
    if round_state['street'] == 'preflop':
      if handType == 1:
        return 'call'
      else:
        return 'raise'
    

    pass

  def receive_game_start_message(self, game_info):
    pass

  def receive_round_start_message(self, round_count, hole_card, seats):
    pass

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    pass

def setup_ai():
  return RandomPlayer()
