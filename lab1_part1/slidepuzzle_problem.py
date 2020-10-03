# Lab 1, Part 1b: Problem Representation.
# Name(s): 

from __future__ import annotations
from typing import Optional, Any, Hashable, Sequence, Iterable, Dict, Union, List, Tuple, NamedTuple

from search_problem import StateNode, Action

#### Lab 1, Part 1b: Problem Representation #################################################

class Coordinate(NamedTuple, Action):
    """ Represents a specific location on the grid with row r and column c
    Can be created with Coordinate(r=row, c=col), or just Coordinate(row,col).
    Properties r and c can be accessed with dot notation or as if a tuple (r,c)

    Is also an Action, representing the coordinate of the tile that is to be moved into 
    the empty space. The first row and column are numbered 0.
    """
    r : int
    c : int

    def __str__(self):
        return "(R:{}, C:{})".format(self.r, self.c)

class SlidePuzzleState(StateNode):
    """ A state node for the slide puzzle environment. """

    # Type Hints allow for the optional type declaration of "instance variables" this way, like Java.
    tiles : Tuple[Tuple[int, ...], ...]
    empty_pos : Coordinate
    
    
    @staticmethod
    def readFromFile(filename : str) -> SlidePuzzleState:
        """Reads data from a text file and returns a SlidePuzzleState which is an initial state.
        The file format is simple: the first line has a number, which is the N, 
        the # of rows/columns of the puzzle (all puzzles are square). 
        There are then N lines with N numbers (space delimited), 
        representing the initial configuration of the tiles in the grid. 
        The number 0 represents the blank tile. 
        """
        with open(filename, 'r') as file:
            # TODO read file and return an initial SlidePuzzleState.
            # This return statement is just a dummy.
            return SlidePuzzleState( 
                tiles = ((0,),), # tuple of tuple of 0, dummy value
                empty_pos = Coordinate(0,0), # dummy value
                parent = None,
                last_action = None,
                depth = 0,
                path_cost = 0,
            )

    #Override
    def __init__(self, 
            tiles : Tuple[Tuple[int, ...], ...],
            empty_pos : Coordinate,
            parent : Optional[StateNode], 
            last_action: Optional[Coordinate], 
            depth : int, 
            path_cost : float = 0.0) :
        """Creates a SlidePuzzleState that represents a state of the environment and context for how the agent gets 
        to this state (the path, aka a series of state-action transitions).
        
        Keyword Arguments:
        All the arguments for StateNode's __init__; Use super.__init__() to call this function and pass appropriate parameters.
        tiles -- a tuple grid of integers representing the position of different numbered tiles
        empty_pos -- a coordinate indicating the position of the empty spot (tile 0)
        """
        super().__init__(parent = parent, last_action = last_action, depth = depth, path_cost = path_cost)
        self.tiles = tiles
        self.empty_pos = empty_pos

    """ Additional accessor methods - needed for the GUI"""

    def get_size(self) -> int:
        """Returns the dimension N of the square puzzle represented which is N-by-N."""
        return len(self.tiles)

    def get_tile_at(self, coord : Coordinate) -> int:
        """ Returns the number of the tile at the given Coordinate.
        If the position is empty, return 0.
        Ideally, this should be done in constant time, not O(N) or O(N^2) time...
        """
        return self.tiles[coord.r][coord.c]

    def get_empty_pos(self) -> Coordinate:
        """Returns Coordinate of the empty tile.
        Ideally, this should be done in constant time, not O(N) or O(N^2) time...
        """
        return self.empty_pos
    
    """ Overridden methods from StateNode """

    # Override
    def get_state_features(self) -> Hashable:
        """Returns a full featured representation of the state. 

        In the case of the slide puzzle, the current positions of all the tiles are the features.
        
        If two SlidePuzzleState objects represent the same state, get_features() should return the same for both objects.
        However, two SlidePuzzleState with identical state features may not represent the same node of the search tree -
        that is, they may have different parents, last actions, path lengths/costs etc...
        """
        return self.tiles

    
    # Override
    def __str__(self) -> str:
        """Return a string representation of the state.
           
           This should return N lines of N numbers each, separated by whitespace,
           similar to the file format for initial states
        """
        n = self.get_size()
        return "\n".join(" ".join("{:2d}".format(self.get_tile_at(Coordinate(r,c))) for c in range(n)) for r in range(n))
    
    # Override
    def is_goal_state(self) -> bool:
        """Returns True if a goal state. 
        The goal of the slide puzzle is to have the empty spot in the 0th row and 0th col,
        and then the rest of the numbered tiles in order down the rows!
        """
        # TODO implement!
        return False
    
    # Override
    def is_legal_action(self, action : Coordinate) -> bool:
        """Returns whether an action is legal from the current state

        Actions in the slide puzzle environment involve moving a tile into
        the adjacent empty spot.
        
        Actions are Coordinate objects, specifying the position of the tile that
        is to be moved into the empty slot. That Coordinate needs to be not out of bounds, and 
        actually adjacent to the emty slot.
        """
        # TODO implement!
        return False
    

    # Override
    def get_all_actions(self) -> Iterable[Coordinate]:
        """Return all legal actions at this state."""
        # TODO implement! This is a good candidate for using yield (generator function)
        yield from ()
        # alternatively, return a list, tuple, or use comprehension
        return []
        

    # Override
    def describe_last_action(self) -> str:
        """Returns a string describing the last_action taken (that resulted in transitioning from parent to this state)
        (Can be None or "None" if the initial state)

        The action should be described as "Moved tile X" where X is the tile number
        that last got slid into the empty spot.
        """
        if self.last_action is None:
             return None 
        return "Moved tile {}".format(self.parent.get_tile_at(self.last_action))

    # Override
    def get_next_state(self, action : Coordinate) -> SlidePuzzleState:
        """ Return a new StateNode that represents the state that results from taking the given action from this state.
        The new StateNode object should have this StateNode (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before), but a ValueError may be passed for illegal actions if desired.
        """
       # TODO implement! Remember that this returns a NEW state, and doesn't change this one.
        return self
        

    """ You may add additional methods that may be useful! """