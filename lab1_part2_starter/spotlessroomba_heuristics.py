from search_heuristics import *
from spotlessroomba_problem import *

INF = float('inf')

def spotlessroomba_first_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial admissible heuristic
    raise NotImplementedError

def spotlessroomba_second_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial consistent heuristic
    raise NotImplementedError

# Make sure to update names below, and add any extra you create.
SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Arbitrary": arbitrary_heuristic, 
                        "Custom Heur. 1 (admissible)": spotlessroomba_first_heuristic,
                        "Custom Heur. 2 (consistent)" : spotlessroomba_second_heuristic
                        }
