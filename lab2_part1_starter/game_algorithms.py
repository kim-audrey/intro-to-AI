# Lab 2: Games (Connect-4, Roomba Race)
# Name(s): Mr. Wang
# Email(s): matwan@bergen.org
# python test_game_gui.py tictactoe initial_states/tictactoe_states/tictactoe_losing.txt
from __future__ import annotations
import sys
from typing import Optional, Any, Hashable, Sequence, Iterable, TypeVar, Dict, Tuple, Callable, Union

import math 
from time import time
from collections import defaultdict # optional, remove later
from gamesearch_problem import StateNode, Action, GameAgent



"""
HELPFUL NOTES:

CODE REPETITION:
Every algorithm in this lab is very similar to the last.
As with the first lab, you'll likely do a lot of copy and paste, with small
(but crucial!) updates between algorithms. This is okay, but this DOES mean you'll
want to be SURE that your earlier algorithms are SOLID before moving forward
(and to apply any later corrections to all your earlier work).

I have attempted to structure the assignment so that there are ways you could leverage inheritance/polymorphism to avoid 
some code copying/reuse, but ultimately there will likely be some unavoidable redundancy.  

RECURSION and HELPER FUNCTIONS:
Every one of the algorithms in this lab use recursion.
You may wish to write "helper" functions/methods for the recursion, since
the parameters and return values of given methods may not be changed, but they may not be 
what parameter and return types you want for recursion.
"""

### Part 0: Reflex Agent ###################

class ReflexAgent(GameAgent):
    """ A "reflex" agent from the perspective of self.player_index.
        Simply looks at the immediately available possible actions, 
        evaluates the value of the resulting states with self.evaluation_fn,
        and returns the best action and its value."""

    player_index : int 
    evaluation_fn : Callable[[StateNode, int], float]

    def __init__(self, 
                player_index : int, 
                evaluation_fn : Callable[[StateNode, int], float],
                *args, **kwargs
                ): 
        self.player_index = player_index
        self.evaluation_fn = evaluation_fn

    #Override
    def pick_action(self, state : StateNode, **kwargs) -> Tuple[Action, Optional[float], Optional[StateNode]]:
        best_action = None
        ba_value = sys.maxsize
        ba_expected_state = None
        

        for a in state.get_all_actions():
            s = state.get_next_state(a)
            s_value = self.evaluation_fn(s, self.player_index)
            if s_value < ba_value:
                ba_value = s_value
                best_action = a
                ba_expected_state = s

        return (best_action, ba_value, ba_expected_state);

        """
        Doesn't do any kind of search, just picks the action that leads to the "best" state, according to self.evaluation_fn.

        Return 2 things (a 3-tuple): (action, value)
        1) an action for the state 
        2) The computed value of taking that action  
        3) The future state that the computed value is derived from
        """


### Part 1: Search Agents: Maximizing, Minimax, AlphaBeta Minimax, Expectimax ###################

class GameSearchAgent(GameAgent):
    """ An abstract class for all kinds of game search agents. """
    # Given at construction
    player_index : int  # The index of the player for the game that this agent represents
    evaluation_fn : Callable[[StateNode, int], float] # The evaluation function for evaluating leaf nodes (both terminal and non-terminal)
    gui_callback_fn : Callable[[StateNode, float, Optional[str]],bool] # Callback fn from the Gui, see below
    depth_limit : Union[int, float] # Max depth to search to

    # For counting nodes visited / evaluations of the last search done.
    total_evals : int
    total_nodes : int
    # For counting nodes visited / evaluations over all searches done over lifetime of agent.
    lifetime_evals : int
    lifetime_nodes : int

    def __init__(self, 
                player_index, evaluation_fn, 
                gui_callback_fn = lambda state, value, notes : False,
                depth_limit = math.inf,
                *args, **kwargs): #any extra arguments, don't worry about 'em
        self.player_index = player_index
        self.evaluation_fn = evaluation_fn
        self.gui_callback_fn = gui_callback_fn
        self.depth_limit = depth_limit
        self.total_nodes, self.total_evals, self.lifetime_nodes, self.lifetime_evals  = 0, 0, 0, 0
        
    def reset_total_counts(self):
        """ Called by the GUI before a search. """
        self.total_nodes = 0
        self.total_evals = 0
    
    def update_lifetime_counts(self):
        """ Called by the GUI after a search. """
        self.lifetime_nodes += self.total_nodes
        self.lifetime_evals += self.total_evals
        
    #Override
    def pick_action(self, state : StateNode) -> Optional[Tuple[Action, float, Optional[StateNode]]]:

        """ To be overridden, possibly, by subclasses.

        Assumes that state.current_player_index == self.player_index. Behavior undefined if that is not the case.

        Chooses an action for this agent to do at the given state by performing a recursive search of the state's subtree up to self.depth_limit, and 
        evaluating leaf states with self.evaluation_fn.

        In the process, you should increment self.total_nodes for every state node visited in the tree, and self.total_evals for every leaf evaluation done.
        
        To visualize the search, self.gui_callback_fn(state, value, notes) should be called at least once for each state visited, along with its computed value and any
        notes you want to show for debugging purposes. 
        At the very least, call the function for a state once its value has been fully computed; if you want to visualize the process partially computed value, 
        you can call the gui_callback_fn at other times too. 
        If the user attempts to terminate the search early, gui_callback_fn will return True. The algorithm should end as quickly as possible, simply returning None.

        Return 3 things (a 3-tuple): (action, value, leaf_node)
        1) an action for the state 
        2) The computed value of the state (and taking that action).
        3) The leaf StateNode that is the source of the computed value. This would be the state at the end of the expected path in the search tree.  
            (Optional, could be None - and for certain subclasses, only makes sense to be None)

        NOTE: There are many, many ways to go about writing this method for the different subclasses. 
        I actually recommend that, for each subclass, you write one or more helper methods 
        that will handle the recursive search. 

        You can then keep this method pretty short, merely calling the recursive search method(s) as needed. 
        You could even implement this method for GameSearchAgent, just *once* for all subclasses, 
        if you utilize inheritance well. 
        *Hint* it could look a lot like ReflexAgent's method...
        """
        # TODO You can actually leave this unimplemented, but if you want to utilize inheritance you may implement it...
        raise NotImplementedError


class MaximizingSearchAgent(GameSearchAgent):
    """
    A search agent that recursively searches the game tree, performing Maximizing Depth First Search.
    All players are modeled as maximizing the utility for self.player_index.
    This could be interpreted as an optimistic model of the other agents' behavior.
    """

    #Override
    def pick_action(self, state : StateNode) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
        EVAL_VAL_INDEX = 1

        self.total_nodes += 1
        if state.depth >= self.depth_limit or state.is_endgame_state():          
            self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index))   
            self.total_evals += 1
            return [state.last_action, self.evaluation_fn(state, self.player_index), state]

        bestul_restul = None
        
        for action in state.get_all_actions():

            restul = self.pick_action(state.get_next_state(action))

            if ((bestul_restul == None) or (restul[EVAL_VAL_INDEX] > bestul_restul[EVAL_VAL_INDEX])):
                bestul_restul = restul
                # bestul_restul[0] = state.last_action

        return bestul_restul
    
class MinimaxSearchAgent(GameSearchAgent):
    """
    A search agent that recursively searches the game tree, performing Maximizing Depth First Search.
    The agent's player_index is modeled as maximizing the utility for self.player_index.
    All other agents are modeled as choosing actions to minimize utility for self.player_index.
    This could be interpreted as being a pessimistic model of the other agents' behavior.
    """
    #Override
    def pick_action(self, state : StateNode) -> Optional[Tuple[Action, float, Optional[StateNode]]]:

        EVAL_VAL_INDEX = 1

        # 4 debugging with gui_callback_fn: nodes_visited = []

        self.total_nodes += 1
        if state.depth >= self.depth_limit or state.is_endgame_state():          
                self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index))   
                self.total_evals += 1
                return [state.last_action, self.evaluation_fn(state, self.player_index), state]

        bestul_restul = None
        
        for action in state.get_all_actions():

            # 4 debugging with gui_callback_fn: nodes_visited.append(state.get_next_state(action))
            restul = self.pick_action(state.get_next_state(action))

            if self.player_index == state.current_player_index:
                if ((bestul_restul == None) or (restul[EVAL_VAL_INDEX] > bestul_restul[EVAL_VAL_INDEX])):
                    bestul_restul = restul
                    bestul_restul[0] = action

            else:
                if ((bestul_restul == None) or (restul[EVAL_VAL_INDEX] < bestul_restul[EVAL_VAL_INDEX])):
                    bestul_restul = restul
                    bestul_restul[0] = action
        

        # 4 debugging with gui_callback_fn: self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index), nodes_visited)

        return bestul_restul

        """ Override GameSearchAgent.pick_action (see the docstring above) 
        Alternatively, remove this if you just want to inherit from GameSearchAgent
        You might write additional helper methods. 
        """

class ExpectimaxSearchAgent(GameSearchAgent):
    """
    A search agent that recursively searches the game tree, performing Maximizing Depth First Search.
    The agent's player_index is modeled as maximizing the utility for self.player_index.
    All other agents are modeled as choosing actions with a uniformly random distribution.
    This could be interpreted as being between an optimistic and pessimistic model of your opponents behavior.
    """
    # #Override
    def pick_action(self, state : StateNode) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
        """ Override GameSearchAgent.pick_action (see the docstring above) 
        Alternatively, remove this if you just want to inherit from GameSearchAgent
        You might write additional helper methods. 

        NOTE: Unlike the other search agents, the expected value is not derived from only one leaf state. 
        So, you can just return None (or anything really) for the third return value, as it will be fairly meaningless.
        """

        EVAL_VAL_INDEX = 1

        # 4 debugging with gui_callback_fn: nodes_visited = []

        self.total_nodes += 1
        if state.depth >= self.depth_limit or state.is_endgame_state():          
                self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index))   
                self.total_evals += 1
                return [state.last_action, self.evaluation_fn(state, self.player_index), None]

        expectul_restul_val = 0
        bestul_restul = None

        for action in state.get_all_actions():

            if self.player_index == state.current_player_index:
                restul = self.pick_action(state.get_next_state(action))

                if ((bestul_restul == None) or (restul[EVAL_VAL_INDEX] > bestul_restul[EVAL_VAL_INDEX])):
                    bestul_restul = restul
                    bestul_restul[0] = action

            else:
                # 4 debugging with gui_callback_fn: nodes_visited.append(state.get_next_state(action))
                restul = self.pick_action(state.get_next_state(action))
                expectul_restul_val += restul[EVAL_VAL_INDEX]
            
            
        return bestul_restul if (self.player_index == state.current_player_index) else ([state.last_action, expectul_restul_val / len(state.get_all_actions()), None])
        

        # 4 debugging with gui_callback_fn: self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index), nodes_visited)



### Part 2: Alpha-Beta Pruning,  #################################################

"""
    Implement AlphaBetaAgent, which is minimax with alpha-beta pruning. 
    It should return the EXACT same result as MinimaxAgent, but will generally search significantly fewer branches
    and thus perform fewer evaluations.
"""

class AlphaBetaSearchAgent(GameSearchAgent):
    """
    Recursively searches the game tree, performing Minimax up to the given depth.
    Uses alpha beta pruning to avoid searching down unnecessary branches.

    You should still call self.gui_callback_fn on cutoffs; for debugging purposes, you might include an optional message indicating that 
    such a cutoff occured.

    In the case of a cutoff, simply return the best action / value seen so far.
    """

    #Override
    def pick_action(self, state : StateNode) -> Optional[Tuple[Action, float, Optional[StateNode]]]:

        def max_value(state, alpha, beta) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
            
            self.total_nodes += 1
            if state.depth >= self.depth_limit or state.is_endgame_state():          
                self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index))   
                self.total_evals += 1
                return [state.last_action, self.evaluation_fn(state, self.player_index), state]

            v = (None, -1 * sys.maxsize)
            minnie = None
            for action in state.get_all_actions():
                succ = state.get_next_state(action)
                minnie = min_value(succ, alpha, beta)                    
                minnie[0] = action

                v = v if (max(v[1], minnie[1]) == v[1]) else minnie
                if v[1] >= beta:
                    return v
                alpha = max(alpha, v[1])
            return v


        def min_value(state, alpha, beta) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
                
            self.total_nodes += 1
            if state.depth >= self.depth_limit or state.is_endgame_state():          
                self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index))   
                self.total_evals += 1
                return [state.last_action, self.evaluation_fn(state, self.player_index), None]

            v = (None, sys.maxsize)
            maxxie = None
            for action in state.get_all_actions():
                succ = state.get_next_state(action)
                maxxie = max_value(succ, alpha, beta)
                maxxie[0] = action
                v = v if (min(v[1], maxxie[1]) == v[1]) else maxxie
                if v[1] <= alpha:
                    return v
                beta = min(beta, v[1])
            return v     


        alpha = -1 * sys.maxsize     # MAX best option
        beta = sys.maxsize     # MIN best option

        restul = max_value(state, alpha, beta)
        return restul;




### Part 3: Iterative Deepening, Transposition Tables & Move Ordering #################################################

"""
Useful functions for this section:
time(): the current system time in seconds. You can measure elapsed time this way
"""

#akljdfsdf
"""
So far, all our search agents are hard commitments - we don't get a usable result until they finish searching to self.depth_limit completely. 
This is not very practical, especially if we have a limited amount of time but don't know how deep we can afford to search. 

Iterative Deepening (or Progressive Deepening) begins with a very shallow search to depth 1, then repeatedly performs deeper searches
with progressively deepening cutoff depths.
It is an "anytime algorithm" because it can be stopped at any
time and be able to yield the best answer it has from the deepest search thus far.
"""

class IterativeDeepeningSearchAgent(GameSearchAgent):
    """ Mixin class for iterative deepening search.
    Since it is a subclass of GameSearchAgent, inherits self.pick_action and self.depth_limit
    """
    
    plateau_cutoff : Union(int, float)

    def __init__(self, 
                plateau_cutoff : Union[int, float], #could be math.inf 
                *args, **kwargs): #any extra arguments, don't worry about 'em
        super().__init__(*args, **kwargs)
        self.plateau_cutoff = plateau_cutoff


    def iterative_pick_action(self, state: StateNode) -> List[Tuple[Action, float, Optional[StateNode]]]: 
        """ Performs an iterative deepening search by calling self.pick_action() repeatedly, starting with self.depth_limit = 1 and incrementing by 1.
        
        Terminates only in two cases:
            1) when self.gui_callback_fn returns True, which may indicate user-termination or the reaching of a time_limit.
            2) when the best action computed by the search has been the same for the past self.plateau_cutoff iterations 

        Instead of just one result tuple, pick_action returns a *list* of tuples. 
        Each element at index i the results of a completed search to depth i+1.
        The results of the search that is terminated mid-way should not be included.

        The results used from the deepest completed search would be used by the caller.
        However, the test GUI will also print out results from each depth.

        NOTE: This should be a very short and simple function. Do NOT reimplement pick_action()
        """

        repeats = 0
        best_picks = []

        i = 1
        while not ((self.gui_callback_fn == True) or (repeats == self.plateau_cutoff)):
            self.depth_limit = i
            best_picks.append(self.pick_action(state))
            i += 1

        return best_picks

"""
    The effectiveness of alpha-beta pruning depends on what order moves are explored.
    If the best moves are explored first at each node, then maximum pruning will occur.

    One way to improve alpha pruning is to incorporate a transposition table for states and best (so far) moves.
    Every time you search a state, save the best move in the table.
    If you encounter that state again (either in the same search, or a later one), you should search that move first.
    After searching the state's children (even if there is a cutoff), update the entry for that state in the table again.

    This is particularly useful when used with iterative deepening, as each shallower search will help re-order future deeper searches for maximum pruning.
"""

class MoveOrderingAlphaBetaSearchAgent(AlphaBetaSearchAgent):

    """
    A subclass of AlphaBetaSearchAgent. 
    Maintains a lifetime transposition table, which saves best actions for any explored states.
    If you encounter a state in the table, begin by searching the saved move first.
    """
    t_table: Dict[StateNode, Action]

    def __init__(self, *args, **kwargs): #any extra arguments, don't worry about 'em
        super().__init__(*args, **kwargs)
        self.t_table = {}

    #Override
    def pick_action(self, state : StateNode) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
        # 4 debugging with gui_callback_fn: 
        nodes_visited = []
        
        def max_value(state, alpha, beta) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
                
            self.total_nodes += 1
            if state.depth >= self.depth_limit or state.is_endgame_state():          
                self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index))   
                self.total_evals += 1

                # 4 debugging with gui_callback_fn: 
                nodes_visited.append(state.get_next_state(state.last_action))

                return [state.last_action, self.evaluation_fn(state, self.player_index), state]

            v = (None, -1 * sys.maxsize)
            minnie = None
            
            if state in self.t_table.keys():
                restul = state.get_next_state(self.t_table[state])
                minnie = min_value(restul, alpha, beta)
                minnie[0] = self.t_table[state]
                v = v if (max(v[1], minnie[1]) == v[1]) else minnie
                if v[1] >= beta:
                    return minnie
                alpha = max(alpha, v[1])

            for action in state.get_all_actions():
                succ = state.get_next_state(action)
                minnie = min_value(succ, alpha, beta)
                minnie[0] = action

                v = v if (max(v[1], minnie[1]) == v[1]) else minnie
                if v[1] >= beta:
                    self.t_table[state] = action
                    return v
                alpha = max(alpha, v[1])
            self.t_table[state] = v[0]

            return v


        def min_value(state, alpha, beta) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
                
            self.total_nodes += 1
            if state.depth >= self.depth_limit or state.is_endgame_state():          
                self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index))   
                self.total_evals += 1
                return [state.last_action, self.evaluation_fn(state, self.player_index), None]

            v = (None, sys.maxsize)
            maxxie = None
            
            if state in self.t_table.keys():
                restul = state.get_next_state(self.t_table[state])
                maxxie = max_value(restul, alpha, beta)
                maxxie[0] = self.t_table[state]
                v = v if (min(v[1], maxxie[1]) == v[1]) else maxxie
                if v[1] <= alpha:
                    return maxxie
                beta = min(beta, v[1])

            for action in state.get_all_actions():
                succ = state.get_next_state(action)
                maxxie = max_value(succ, alpha, beta)
                maxxie[0] = action
                v = v if (min(v[1], maxxie[1]) == v[1]) else maxxie
                if v[1] <= alpha:
                    self.t_table[state] = action
                    return v
                beta = min(beta, v[1])
            self.t_table[state] = v[0]
            return v     

        
        # 4 debugging with gui_callback_fn: 
        self.gui_callback_fn(state, self.evaluation_fn(state, self.player_index), nodes_visited)
        
        alpha = -1 * sys.maxsize     # MAX best option
        beta = sys.maxsize     # MIN best option

        restul = max_value(state, alpha, beta)

        print(self.t_table)
        return restul;
            



### EXTENSION: Monte Carlo Tree Search #################################################

"""
EXTENSION - 
This is for those who want to challenge themselves.
MCTS a beautiful algorithm, but more complex than the rest of the lab!
"""

class MonteCarloTreeSearchAgent(GameAgent):
    # Given at construction
    player_index : int  # The index of the player for the game that this agent represents
    gui_callback_fn : Callable[[StateNode, float, Optional[str]],bool] # Callback fn from the Gui, see below
    exploration_bias : float # Constant that encourages exploration of less simulated nodes.

    # For counting rollouts during the last search.
    total_rollouts : int
    # For counting rollouts over all searches done over lifetime of agent.
    lifetime_rollouts : int

    def __init__(self, 
                player_index,
                exploration_bias : float,
                gui_callback_fn = lambda state, value, notes : False,                
                *args, **kwargs): #any extra arguments, don't worry about 'em
        super().__init__(*args, **kwargs)
        self.player_index = player_index
        self.exploration_bias = exploration_bias
        self.gui_callback_fn = gui_callback_fn
        self.total_rollouts, self.lifetime_rollouts = 0, 0
        
    def reset_total_counts(self):
        """ Called by the GUI before a search. """
        self.total_rollouts = 0
    
    def update_lifetime_counts(self):
        """ Called by the GUI after a search. """
        self.lifetime_rollouts += self.total_rollouts
        

    # Override
    def pick_action(self, state : StateValue) -> Optional[Tuple[Action, float, Optional[StateNode]]]:
        #TODO 
        raise NotImplementedError
