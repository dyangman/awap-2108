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
    Returns node of least resistance
    """
    def best_node_advantage(self, node):
        # TODO: If there is a tie, favor the closer one to your center
        best_advantage = 0
        best_neighbor = None
        node_owner = self.board.nodes[node]['owner']
        node_units = self.board.nodes[node]['old_units']
        for neighbor in self.board[node]:
            if node_owner == self.board.nodes[neighbor]['owner']:
                continue

            neighbor_units = self.board.nodes[neighbor]['old_units']
            advantage = node_units - neighbor_units

            if best_neighbor is None or advantage > best_advantage:
                best_advantage = advantage
                best_neighbor = neighbor

        return best_neighbor, best_advantage


    """
    Determines if node is adjacent to an enemy
    """
    def is_threatened_node(self, node):
        node_owner = self.board.nodes[node]['owner']
        for neighbor in self.board[node]:
            neighbor_owner = self.board.nodes[neighbor]['owner']
            if neighbor_owner != None and neighbor_owner != node_owner:
                return True
        return False


    """
    Determines if node is on the frontier
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
                players[node_owner] = {'total_units' : 0, 'frontier_nodes' : 0, 'total_nodes' : 0, 'frontier_units' : 0, 'threatened_nodes' : 0}
        
            players[node_owner]['total_nodes'] += 1
            players[node_owner]['total_units'] += node_units

            if self.is_frontier_node(node):
                players[node_owner]['frontier_nodes'] += 1
                players[node_owner]['frontier_units'] += node_units

            if self.is_threatened_node(node):
                players[node_owner]['threatened_nodes'] += 1

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
        
        frontier_nodes = []

        for node in self.nodes:
            if self.is_frontier_node(node):
                frontier_nodes.append(node)

        possible_targets = []
        for frontier_node in frontier_nodes:
            node, advantage = self.best_node_advantage(frontier_node)
            possible_targets.append((frontier_node, node, advantage))

        possible_targets = sorted(possible_targets, key=lambda x: x[2], reverse=True)

        print(possible_targets)

        available_units = self.max_units
        print('Available')
        print(available_units)
        for target in possible_targets:
            advantage = target[2]
            if advantage <= 2:
                required_units = 2 - advantage
                
                if available_units > required_units:
                    # print('Placed ' + str(required_units) + ' at ' + str(target[0]))
                    self.place_unit(target[0], required_units)
                    available_units -= required_units
                else:
                    # print('Placed ' + available_units + ' at ' + str(target[0]))
                    self.place_unit(target[0], available_units)
                    available_units = 0

        print('remaining')
        print(available_units)

        # Place remaining somewhere
        for node in self.nodes:
            self.place_unit(node, available_units)
            break

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """

        frontier_nodes = []

        for node in self.nodes:
            if self.is_frontier_node(node):
                frontier_nodes.append(node)

        possible_targets = []
        for frontier_node in frontier_nodes:
            node, advantage = self.best_node_advantage(frontier_node)
            possible_targets.append((frontier_node, node, advantage))

        for target in possible_targets:


            friendly_units = self.board.nodes[target[0]]['old_units']
            enemy_units = self.board.nodes[target[1]]['old_units']

            # print('Info')
            # print(target)
            # print(friendly_units)
            # print(enemy_units)

            if friendly_units >= enemy_units + 2:
                self.move_unit(target[0], target[1], enemy_units + 1)            

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
