#!/usr/bin/env python3

"""
Sudoku has grid size of 9x9
each cell of grid has number
every cell in a same row must have a distinguished number
every cell in a same column must have a distinguished number
we divide grid by small chunk of square has size of 3x3,
    and every cell of grid must be an element of a chunk at least.
Suppose we have two arbitary chunks called c1 and c2 (and c1!=c2), then
    a product set of c1 and c2 is always an empty set.
For any chunk, it must have 9 cells have distinguished number
"""

class Sudoku:
    column = 'abcdefghi'
    row = '123456789'
    info = {} # it contains number of given block. (number is 0 if number is not given) @key: block_name @value: number
    numGroup = []
    grid = []

    def __init__(self, exist=None):
        self.grid = [[None for x in range(9)] for y in range(9)]
        initialize()

    def initialize(self):
        # create a unique name of cell by compounding column and row and initialize info dict.
        for r in row:
            for c in column:
                key = r+c
                info[key] = 0 # initialize with 0
        # create a list of cells have same row
        for r in row:
            temp = []
            for c in column:
                temp.append(r+c)
        
            
                


    def initSet(self):
        for y in range(9):
            for x in range(9):
                self.grid[y][x] = {'row' = [grid[y][r] for r in range(9)],
                        'column' = [grid[c][x] for c in range(9)],
                        'chunk' = [grid[c][


    def printGrid(self):
        # print grid
                        
    def load(self, grid):
        # this puts value on self.grid from the given grid.
    

sudo = Sudoku()
sudo.printGrid()
