from MCTS.heuristic_mcts import Node
class PokerGame(_CARDS, Node): #PokerGame is a child class of Node,


    def find_children(self):
        "All possible successors of this board state"
        return set()


    def find_rational_child(self):
        #to do
        "a good successor of this board state (for more rational simulation)"
        return None


    def is_terminal(self):
        "Returns True if the node has no children"
        return True


    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0


    def __hash__(self):
        "Nodes must be hashable"
        return 123456789


    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True

