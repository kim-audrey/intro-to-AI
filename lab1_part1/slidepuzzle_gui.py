from __future__ import annotations
from typing import *
from tkinter import filedialog, Tk
from os import getcwd
from sys import argv
from slidepuzzle_problem import *
from slidepuzzle_heuristics import SLIDEPUZZLE_HEURISTICS
from search_algorithms import ALGORITHMS, STRATEGIES
from search_gui import Search_GUI, Search_GUI_Controller

### State visualization too big? Change these numbers
MAX_HEIGHT = 450
MAX_WIDTH = 450

TILE, EMPTY, PATH, TEXT = 'tile', 'empty', 'path', 'text'
COLORS = {TILE : 'tan', EMPTY : 'white', PATH: 'IndianRed1', TEXT: 'black'}

class SlidePuzzle_GUI(Search_GUI):

    current_state : SlidePuzzleState

    def __init__(self, initial_state : SlidePuzzleState, algorithm_names : Sequence[str], strategy_names : Sequence[str], heuristics : Dict[str,Callable[[StateNode], float]]):
        self.puzzle_dim = initial_state.get_size()
        super().__init__(canvas_height = MAX_HEIGHT, canvas_width = MAX_WIDTH, algorithm_names = algorithm_names , strategy_names = strategy_names, heuristics = heuristics)
        self.title("Slide Puzzle Search Visualizer")

    def calculate_box_coords(self, r : int, c : int) -> Tuple[int, int, int, int]:
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x1 = w * c // self.puzzle_dim
        y1 = h * r // self.puzzle_dim
        x2 = w * (c + 1) // self.puzzle_dim
        y2 = h * (r + 1) // self.puzzle_dim
        return (x1, y1, x2, y2)

    def calculate_center_coords(self, r : int, c : int) -> Tuple[int, int]:
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        x = int(w * (c + .5)) // self.puzzle_dim
        y = int(h * (r + .5)) // self.puzzle_dim
        return (x, y)

    #Override
    def draw_state(self):
        self.canvas.delete(TEXT)
        self.canvas.delete(EMPTY)
        self.canvas.delete(PATH)

        # roomba agent

        # draw number tiles and empty tile
        text_size = self.canvas.winfo_height() // (self.puzzle_dim * 2)
        for r in range(0,self.puzzle_dim):
            for c in range(0,self.puzzle_dim):
                tile = self.current_state.get_tile_at(Coordinate(r,c))
                pos = self.calculate_center_coords(r,c)
                if tile != 0 :
                    self.canvas.create_text(pos, fill = COLORS[TEXT], tag = TEXT,
                        text = str(tile), font = ('Times New Roman', text_size, 'bold' ))
                else :
                    x1, y1, x2, y2 = self.calculate_box_coords(r,c)
                    self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill= COLORS[EMPTY], tag=EMPTY)

        if self.current_state.depth > 0:
            self.draw_path()
    
    #Override
    def draw_path(self):
        path_coords = [self.calculate_center_coords(*state.get_empty_pos())
                        for state in self.current_state.get_path() ]
        self.canvas.create_line(path_coords, fill = COLORS[PATH], width = 4, tag=PATH)
        
    #Override
    def draw_background(self):

        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        # Clear the background grid and tiles
        self.canvas.delete('grid_line')
        self.canvas.delete(TILE)

        # Draw all the "tiles" - really, background color
        self.canvas.create_rectangle(0, 0, w, h, fill= COLORS[TILE], tag=TILE)

        # Creates all vertical lines
        for c in range(0, self.puzzle_dim):
            x = w * c // self.puzzle_dim
            self.canvas.create_line([(x, 0), (x, h)], tag='grid_line', width = 3)

        # Creates all horizontal lines
        for r in range(0, self.puzzle_dim):
            y = h * r // self.puzzle_dim
            self.canvas.create_line([(0, y), (w, y)], tag='grid_line', width = 3)


    def click_canvas_to_action(self, event) -> Coordinate:
        w = self.canvas.winfo_width() # Get current width of canvas
        col = event.x // (w //  self.puzzle_dim)
        h = self.canvas.winfo_height() # Get current height of canvas
        row = event.y // (h //  self.puzzle_dim)
        # print('clicked {}'.format(col))
        return Coordinate(row, col)


if __name__ == "__main__":
    if len(argv) > 1:
        file_path = argv[1]
    else: 
        initroot = Tk()
        initroot.withdraw()
        file_path = filedialog.askopenfilename(title = "Open Slide Puzzle File",initialdir = getcwd(), filetypes=[("SlidePuzzle", ".slidepuzzle"), ("Text", ".txt")])
        initroot.destroy()
    initial_state = SlidePuzzleState.readFromFile(file_path)
    gui = SlidePuzzle_GUI(initial_state,algorithm_names=ALGORITHMS.keys(), strategy_names=STRATEGIES.keys(), heuristics=SLIDEPUZZLE_HEURISTICS)
    controller = Search_GUI_Controller(gui, initial_state, SLIDEPUZZLE_HEURISTICS)
    gui.mainloop()