from base_player import BasePlayer
import networkx as nx

class Player(BasePlayer):

    """
    You will implement this class for the competition.
    You can add any additional variables / methods in this file. 
    Do not modify the class name or the base class and do not modify the lines marked below.
    """

    def __init__(self, p_id):
        super().__init__(p_id)  #Initializes the super class. Do not modify!

        """
        Insert player-specific initialization code here
        """
        return

    """
    Returns the statistics on each player
    """
    def is_frontier_node(self, node):
        for neighbor in self.board[node]:
            if self.board.nodes[node]['owner'] != self.board.nodes[neighbor]['owner']:
                return True
        return False


    """
    Returns the statistics on each player
    """
    def find_player_stats(self):
        players = {}

        for node in self.board.nodes:
            node_owner = self.board.nodes[node]['owner']
            node_units = self.board.nodes[node]['old_units']

            # Skip unoccupied nodes
            if node_owner is None:
                continue

            # Initalize dictionary for each player
            if node_owner not in players:
                players[node_owner] = {'Total Units' : 0, 'Frontier Nodes' : 0, 'Total Nodes' : 0}
        
            players[node_owner]['Total Units'] += node_units
            players[node_owner]['Total Nodes'] += 1

            if self.is_frontier_node(node):
                players[node_owner]['Frontier Nodes'] += 1

        return players


    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables

        """
        Insert any player-specific turn initialization code here
        """
        return


    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        """
        Insert player logic here to determine where to place your units
        """
        
        for node in self.nodes:
            self.place_unit(node, self.max_units)
            break

        print(self.find_player_stats())

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
