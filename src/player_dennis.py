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
        
        self.turns = 0

        return


    """
    Returns most threatening node
    """
    def worst_node_threat(self, node):
        worst_threat = None
        node_owner = self.board.nodes[node]['owner']
        node_units = self.board.nodes[node]['old_units']

        for neighbor in self.board[node]:
            neighbor_owner = self.board.nodes[neighbor]['owner']
            if node_owner == neighbor_owner or neighbor_owner is None:
                continue

            neighbor_units = self.board.nodes[neighbor]['old_units']

            advantage = node_units - neighbor_units
            if worst_threat is None or advantage < worst_threat:
                worst_threat = advantage

        return worst_threat


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

        self.turns += 1

        return


    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        """
        Insert player logic here to determine where to place your units
        """

        possible_targets = []
        possible_fortifications = []

        for node in self.nodes:
            if self.is_frontier_node(node):
                enemy_node, advantage = self.best_node_advantage(node)
                possible_targets.append((node, enemy_node, advantage))
            if self.is_threatened_node(node):
                threat = self.worst_node_threat(node)
                possible_fortifications.append((node, threat))

        possible_targets = sorted(possible_targets, key=lambda x: x[2], reverse=True)
        possible_fortifications = sorted(possible_fortifications, key=lambda x: x[1], reverse=True)

        available_units = self.max_units
        # print('Placing %d' % available_units)

        print(possible_fortifications)
        for node, threat_level in possible_fortifications:
            if threat_level > 0:
                continue
            required = 1 - threat_level
            if required <= available_units:
                self.place_unit(node, required)
                available_units -= required
            else:
                self.place_unit(node, available_units)
                available_units = 0

        for current_node, target_node, advantage in possible_targets:
            
            if advantage <= 2:
                required_units = 2 - advantage
                
                if available_units > required_units:
                    self.place_unit(current_node, required_units)
                    available_units -= required_units
                else:
                    self.place_unit(current_node, available_units)
                    available_units = 0

        # print('remaining')
        if available_units > 0:
            for node, threat_level in possible_fortifications:
                self.place_unit(node, available_units)
                available_units = 0
                break

        # Place remaining somewhere
        if available_units > 0:
            for node in self.nodes:
                self.place_unit(node, available_units)
                available_units = 0
                break

        print(available_units)
            # print('Options')
            # print(frontier_nodes)
            # for current_node, target_node, advantage in possible_targets:
            #     print("%d %d %d" % (current_node, target_node, advantage))

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """

        possible_targets = []

        for node in self.nodes:
            if self.is_frontier_node(node):
                enemy_node, advantage = self.best_node_advantage(node)
                possible_targets.append((node, enemy_node, advantage))

        owned_nodes = self.find_player_stats()[self.player_num]['total_nodes']

        mod_term = 0

        if owned_nodes >= 22 : 
            mod_term = owned_nodes - 17
        elif owned_nodes == 12 or owned_nodes == 16 : 
            mod_term = 5
        elif owned_nodes == 13 or owned_nodes == 17 : 
            mod_term = 4
        elif owned_nodes == 14 or owned_nodes == 18 or owned_nodes == 19 :
            mod_term = 3
        elif owned_nodes == 15 or owned_nodes == 20 or owned_nodes == 21 : 
            mod_term = 1
        else:
            mod_term = 0

        if self.turns > 180:
            mod_term = 0

        mod_term *= 1000

        for node, enemy_node, advantage in possible_targets:

            friendly_units = self.board.nodes[node]['old_units']
            enemy_units = self.board.nodes[enemy_node]['old_units']
            enemy_owner = self.board.nodes[enemy_node]['owner']

            if enemy_owner is None:
                if friendly_units >= enemy_units + 2 + mod_term:
                    move_units = enemy_units + 1
                    self.move_unit(node, enemy_node, move_units)
            else:
                if (friendly_units > enemy_units + 2 + mod_term):
                    move_units = enemy_units + 1
                    if (int)(friendly_units / 2) >= (enemy_units + 1) + mod_term:
                        move_units = (int)(friendly_units / 2)
                    self.move_unit(node, enemy_node, move_units)

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
