# Lab 1, Part 2a: Heuristics.
# Name(s): 
from search_heuristics import *
from slidepuzzle_problem import *

INF = float('inf')

#### Lab 1, Part 2a: Heuristics #################################################

# Implement these two heuristic functions for SlidePuzzleState.

""" Return the Hamming distance (number of tiles out of place) of the SlidePuzzleState """
def slidepuzzle_hamming(state : SlidePuzzleState)  -> float:
    num=0
    ham=0
    for row in state.tiles:
        for col in row:
            if(col!=num):
                ham+=1
            num+=1
    return ham

""" Return the sum of Manhattan distances between tiles and goal of the SlidePuzzleState """
def slidepuzzle_manhattan(state : SlidePuzzleState)  -> float:
    num=0
    man=0
    
    for currX in range(len(state.tiles)):
        row = state.tiles[currX]

        for currY in range (len(row)):
            col = row[currY]

            if (num != col):
                goalX= (int)(col % len(row))
                goalY= (int)(col / len(row))
                man += abs(goalX - currX) + abs(goalY - currY)
            num += 1
    return man            
            




[[0,1,2], [3,4,5], [4,5], [6,7]]

SLIDEPUZZLE_HEURISTICS = {
    "Zero" : zero_heuristic, 
    "Arbitrary": arbitrary_heuristic, 
    "Hamming" : slidepuzzle_hamming,
    "Manhattan" : slidepuzzle_manhattan
    }

