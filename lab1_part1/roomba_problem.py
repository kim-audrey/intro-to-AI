from __future__ import annotations
from typing import Optional, Tuple, Dict, Any, Hashable, Sequence, Iterable, NamedTuple, TypeVar

from search_problem import StateNode, Action

Terrain = TypeVar('Terrain', bound=str)

FLOOR : Terrain = '.'
CARPET  : Terrain = '~'
WALL : Terrain = '#'
DIRTY_FLOOR : Terrain = '?'
DIRTY_CARPET : Terrain = '+'

"""The cost to move onto different types of terrain."""
TRANSITION_COSTS : Dict[Terrain, float]= {FLOOR: 1, CARPET: 2, WALL: 0, DIRTY_FLOOR: 1, DIRTY_CARPET: 2}

class Coordinate(NamedTuple, Action):
    """ Represents a specific location on the grid with row r and column c
    Can be created with Coordinate(r=row, c=col), or just Coordinate(r,c).
    Properties r and c can be accessed with dot notation or as if a tuple (r,c)
    
    Is also an Action, representing the *relative* coordinate a Roomba is trying to move - that is, the 
    number of rows down and columns right the roomba is trying to move. 
    """
    row : int
    col : int

    def __str__(self):
        return "(R:{}, C:{})".format(self.row, self.col)
    
def add(c1 : Coordinate, c2 : Coordinate) -> Coordinate:
    return Coordinate(row = c1.row + c2.row, col = c1.col + c2.col)

"""All the directions the roomba position can move, and their names."""
ALL_ACTIONS : Tuple[Coordinate] = (Coordinate(0,1), Coordinate(1,0), Coordinate(0, -1), Coordinate(-1,0))
ACTION_NAMES : Dict[Coordinate, str] = {Coordinate(0,1): "East", Coordinate(1,0): "South", Coordinate(0, -1): "West", Coordinate(-1,0): "North"}
class RoombaState(StateNode):
    """
    An immutable representation of the state of a Roomba Route environment. 
    In such an environment, the roomba moves around a grid with the goal of 
    finding the (or a) dirty spot to clean. 
    """

    """ Type Hints allow for the optional type declaration of "instance variables" this way, like Java """
    position : Coordinate
    grid : Tuple[Tuple[Terrain,...],...]

    #Override
    @staticmethod
    def readFromFile(filename : str) -> RoombaState:
        """Reads data from a text file and returns a RoombaState which is an initial state."""
        with open(filename, 'r') as file:
            # First line has the number of rows and columns in the environment's grid
            max_r, max_c = (int(x) for x in file.readline().split())
            # Second line has the initial row/column of the roomba agent
            init_r, init_c = (int(x) for x in file.readline().split())
            # Remaining lines are the layout grid of the environment
            grid = tuple( tuple(file.readline().strip()) for r in range(max_r))
            # Sanity check - is the grid really the right size?
            assert (len(grid) == max_r and all( len(row) == max_c for row in grid))

            return RoombaState(position = Coordinate(init_r, init_c),
                                grid = grid,
                                parent = None,
                                last_action = None,
                                depth = 0,
                                path_cost = 0)
    
    #Override
    def __init__(self, 
                position: Tuple[int, int], 
                grid: Tuple[Tuple[Terrain,...],...], 
                parent : Optional[RoombaState], 
                last_action: Optional[Coordinate],  #Note that actions are (relative) Coordinates!
                depth : int, 
                path_cost : float = 0.0) :
        """
        Creates a RoombaState, which represents a state of the roomba's environment .

        Keyword Arguments (in addition to StateNode arguments):
        position: Coordinate of roomba agent's current row/col.
        grid: 2-d Tuple grid of Terrains, representing the maze.
        """
        super().__init__(parent = parent, last_action = last_action, depth = depth, path_cost = path_cost)
        self.position = position
        self.grid = grid


    """ Additional accessor methods """
    
    def get_width(self) -> int:
        """Returns the width (number of cols) of the maze"""
        return len(self.grid[0])

    def get_height(self) -> int:
        """Returns the height (number of rows) of the maze"""
        return len(self.grid)

    def is_inbounds(self, coord : Coordinate) -> bool:
        return (coord.row >= 0) and (coord.col  >= 0) and (coord.row < self.get_height()) and (coord.col < self.get_width())
    
    def get_terrain(self, coord : Coordinate) -> Terrain:
        return self.grid[coord.row][coord.col]


    """ Overridden methods from StateNode """

    # Override
    def get_state_features(self) -> Hashable:
        """Returns a full feature representation of the state.
        Since the grid is the same for all possible states in this environment
        the position alone is sufficient to distinguish between states.

        If two RoombaState objects represent the same state, get_features() should return the same for both objects.
        However, two RoombaState with identical state features may not represent the same node of the search tree -
        that is, they may have different parents, last actions, path lengths/costs etc...
                """
        return (self.position)

    # Override
    def __str__(self) -> str:
        """Return a string representation of the state."""
        s = "\n".join("".join(row) for row in self.grid)
        ## Draw the roomba agent at the correct position.
        pos = self.position.row * (self.get_width()+1) + self.position.col
        return s[:pos] + 'X' + s[pos+1:] + "\n" # 

    # Override
    def is_goal_state(self) -> bool:
        """Returns if a goal (terminal) state."""
        return self.get_terrain(self.position) in (DIRTY_FLOOR, DIRTY_CARPET)

    # Override
    def is_legal_action(self, action : Coordinate) -> bool:
        """Returns whether an action is legal from the current state"""
        newpos = add(self.position, action)
        return self.is_inbounds(newpos) and self.get_terrain(newpos) != WALL

    # Override
    def get_all_actions(self) -> Iterable[Coordinate]:
        """Return all legal actions from this state. Actions are (relative) Coordinates."""
        for action in ALL_ACTIONS:
            if self.is_legal_action(action):
                yield action
        ### The above generator definition is equivalent to:
        # return (a for a in ALL_ACTIONS if self.is_legal_action(a))
        ### If it is better to get a List for the reusability, methods, or indexing:
        # return [a for a in ALL_ACTIONS if self.is_legal_action(a)]

    # Override
    def describe_last_action(self) -> str:
        """Returns a string describing the last_action taken (that resulted in transitioning from parent to this state)
        (None if the initial state)
        """
        return ACTION_NAMES.get(self.last_action, None)

    # Override
    def get_next_state(self, action : Coordinate) -> RoombaState:
        """ Return a new RoombaState that represents the state that results from taking the given action from this state.
        The new RoombaState object should have this (self) as its parent, and action as its last_action.

        -- action is assumed legal (is_legal_action called before)
        """
        new_pos = add(self.position, action)
        step_cost = TRANSITION_COSTS[self.get_terrain(new_pos)]
        return RoombaState( position = new_pos,
                                grid = self.grid, # The grid doesn't change from state to state
                                last_action = action,
                                parent = self,
                                depth = self.depth + 1,
                                path_cost = self.path_cost + step_cost)