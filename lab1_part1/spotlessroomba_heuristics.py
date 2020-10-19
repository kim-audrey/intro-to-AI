from lab1_part1.spotlessroomba_problem import SpotlessRoombaState
from os import system
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

#This firstly finds the hamming distance to the closest spot, doing this garuntees it goes to the closest one which is most effiecient. Afterwards it assumes the distance to each other dirty space is 1 in order to underestimate. It's basically just hamming with a few extra steps.
def spotlessroomba_first_heuristic(state : SpotlessRoombaState)  -> float:
    heuri = 0

    lowest = system.maxint
    for tup in state.dirty_locations:
        ham = abs(tup[0] - state.position[0]) + abs(tup[1] - state.position[1])
        if ham < lowest:
            lowest = ham
    lowest += len(state.dirty_locations)-1
    heuri += lowest

    return heuri
        




def spotlessroomba_second_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial consistent heuristic
    raise NotImplementedError

# This gorgeous beutiful masterpiece of a heuristic is technically nontrivial as it isn't always zero. However it uses the same concept as the zero hueristic, saying we are always 1 away from the goal unless we are the goal state. True beauty. This hueristic is made by Alex and only Alex,
def silly_heuristic(state:SpotlessRoombaState) ->float:
    if(state.is_goal_state):
        return 0
    return 1

# Make sure to update names below, and add any extra you create.
SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Arbitrary": arbitrary_heuristic, 
                        "Custom Heur. 1 (admissible)": spotlessroomba_first_heuristic,
                        "Custom Heur. 2 (consistent)" : spotlessroomba_second_heuristic,
                        "Silly" : silly_heuristic
                        }



# edit this obvi
ROOMBA_HEURISTICS = {
    "Zero" : zero_heuristic, 
    "Arbitrary": arbitrary_heuristic, 
    "Manhattan Dist. (one goal)" : roomba_manhattan_onegoal,
    "Manhattan Dist. (closest)" : roomba_manhattan_multigoal
    }
