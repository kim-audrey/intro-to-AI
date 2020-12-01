import sys
import math
from spotlessroomba_problem import SpotlessRoombaState
from search_heuristics import *
from spotlessroomba_problem import *

INF = float('inf')

"""
RULES FOR HEURISTICS:

BOTH
- nontrivial
- admissible (never overestimates)
-  look at fewer states than UCS, especially in bigger mazes
1. ADMISSIBLE --  If the sum is bobbing up and down, your heuristic is not admissible!  (must be steadily increasing)
2. CONSISTENT --  heuristic must never overestimate the distance to the goal, 
                AND for any transition from s to s’ that costs c, heuristic h must satisfy the equation h(s) - h(s’) <= c (or, h(s)  <= h(s’) + c)


1. [dirty locations left] [hamming to closest]
"""

# Firstly, this hueristic adds the amount of dirty spots left, as you need to move at least as many times as 
# dirty spaces left. This means the hueristic is always consistent. Them, the manhattan distance to the nearest 
# dirty spot is found, as going to the closest one is always optimal. This is scaled down so that it is less 
# important than the amount of dirtly locations, which directly influences how close we are.
def spotlessroomba_first_heuristic(state : SpotlessRoombaState)  -> float:

    if state.is_goal_state():
        return 0

    heuri = len(state.dirty_locations)

    lowest = sys.maxsize
    for tup in state.dirty_locations:
        if tup == state.position:
            heuri-=1
        man = abs(tup[0] - state.position[0]) + abs(tup[1] - state.position[1])
        if man < lowest:
            lowest = man
    heuri += lowest * .01

    return heuri
        
# The same as the first heuristic but instead of manhattan it
def spotlessroomba_second_heuristic(state : SpotlessRoombaState)  -> float:
    if state.is_goal_state():
            return 0

    heuri = len(state.dirty_locations)

    lowest = sys.maxsize
    for tup in state.dirty_locations:
        if tup == state.position:
            heuri-=1
        ham = math.hypot((tup[0] - state.position[0]), (tup[1] - state.position[1]))
        if ham < lowest:
            lowest = ham
    heuri += lowest * .01

    return heuri


# This gorgeous beutiful masterpiece of a heuristic is technically nontrivial as it isn't always zero. 
# However it uses the same concept as the zero hueristic, saying we are always 1 away from the goal unless we 
# are the goal state. True beauty. This hueristic is made by Alex and only Alex,
def silly_heuristic(state:SpotlessRoombaState) ->float:
    if(state.is_goal_state()):
        return 0
    return 1


SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Arbitrary": arbitrary_heuristic, 
                        "Multi-Man": spotlessroomba_first_heuristic,
                        "Multi-Ham" : spotlessroomba_second_heuristic,
                        "Silly" : silly_heuristic
                        }