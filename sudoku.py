#!/usr/bin/env python3

import logging
import time

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
    subCol = ['abc','def','ghi']
    subRow = ['123','456','789']
    info = {} # it contains cell's number. (number is 0 if number is not given) @key: cell @value: number
    distinct = [] # it contains a list has cells are distinct by its value
    check = {} # @key: cell @value: list of distinct's indices. each index points a list that given cell is in

    #test purpose
    tracking = []
    tracking_grid = []

    def __init__(self, exist=None):
        self.grid = [[None for x in range(9)] for y in range(9)]
        self.initialize()

    def debug(self):
        print('column: '+self.column)
        print('row: '+self.row)
        print('info: {}'.format(self.info))
        print('distinct:')
        for d in self.distinct:
            print('distinct[{}]: {}'.format(self.distinct.index(d),d))
        print('check: {}'.format(self.check))

    def print(self,grid=None):
        if(grid==None):
            grid = self.info.copy()
        for key in grid.keys():
            if(grid[key]==0 or type(grid[key]) is list):
                grid[key] = '.'
        print(' _______________________ ')
        print('|       |       |       |')
        print('| {1a} {2a} {3a} | {4a} {5a} {6a} | {7a} {8a} {9a} |'.format_map(grid))
        print('| {1b} {2b} {3b} | {4b} {5b} {6b} | {7b} {8b} {9b} |'.format_map(grid))
        print('| {1c} {2c} {3c} | {4c} {5c} {6c} | {7c} {8c} {9c} |'.format_map(grid))
        print('|_______|_______|_______|')
        print('|       |       |       |')
        print('| {1d} {2d} {3d} | {4d} {5d} {6d} | {7d} {8d} {9d} |'.format_map(grid))
        print('| {1e} {2e} {3e} | {4e} {5e} {6e} | {7e} {8e} {9e} |'.format_map(grid))
        print('| {1f} {2f} {3f} | {4f} {5f} {6f} | {7f} {8f} {9f} |'.format_map(grid))
        print('|_______|_______|_______|')
        print('|       |       |       |')
        print('| {1g} {2g} {3g} | {4g} {5g} {6g} | {7g} {8g} {9g} |'.format_map(grid))
        print('| {1h} {2h} {3h} | {4h} {5h} {6h} | {7h} {8h} {9h} |'.format_map(grid))
        print('| {1i} {2i} {3i} | {4i} {5i} {6i} | {7i} {8i} {9i} |'.format_map(grid))
        print('|_______|_______|_______|')

    def initialize(self):
        # create a unique name of cell by compounding column and row and initialize info dict.
        for r in self.row:
            for c in self.column:
                key = r+c
                self.info[key] = 0 # initialize with 0
                self.check[key] = [] # initialize with empty list
        # create a list of cells have same row and column
        for r in self.row:
            temp = []
            for c in self.column:
                temp.append(r+c)
            self.distinct.append(temp)
            index = self.distinct.index(temp)
            for c in self.column:
                self.check[r+c].append(index)
        for c in self.column:
            temp = []
            for r in self.row:
                temp.append(r+c)
            self.distinct.append(temp)
            index = self.distinct.index(temp)
            for r in self.row:
                self.check[r+c].append(index)
        for sr in self.subRow:
            for sc in self.subCol:
                temp = []
                for r in sr:
                    for c in sc:
                        temp.append(r+c)
                self.distinct.append(temp)
                index = self.distinct.index(temp)
                for r in sr:
                    for c in sc:
                        self.check[r+c].append(index)

    def update(self,key,value):
        if(self.info.get(key)!=None):
            if(type(self.info.get(key)) is int):
                if(value <= 9 and value >= 0):
                    self.info[key] = value
                else:
                    logging.warning('invalid value({}). the value must be in between 0 and 9'.format(value))
            else:
                logging.warning('invalid value({}). the value must be integer'.format(value))
        else:
            logging.warning('invalid key({}). please see README to use a correct key'.format(key))

    def insert(self,lst): #lst is a list of a row-wise traversal of Sudoku grid.
        if(len(lst)==81): # if lst is a list only contains numbers
            index = 0
            info = self.info.copy()
            for c in self.column:
                for r in self.row:
                    value = lst[index]
                    if(type(value) is int):
                        if(value <= 9 and value >= 0):
                            info[r+c] = value
                        else:
                            logging.warning('invalid number({}) at index number {}. the value must be in between 0 and 9'.format(value,index))
                            return
                    else:
                        logging.warning('invalid value({}) at index number {}. the value must be integer'.format(value,index))
                        return
                    index = index+1
            self.info = info
        elif(len(lst)==9): #if lst has sublists (row-wise)
            index = 0
            info = self.info.copy()
            for c in self.column:
                sublst = lst[index]
                if(len(sublst)==9): # each sublist must have 9 numbers
                    subIndex = 0
                    for r in self.row:
                        value = sublst[subIndex]
                        if(type(value) is int):
                            if(value <= 9 and value >= 0):
                                info[r+c] = value
                            else:
                                logging.warning('invalid number({}) at index number [{}][{}]. the value must be in between 0 and 9'.format(value,index,subIndex))
                                return
                        else:
                            logging.warning('invalid value({}) at index number [{}][{}]. the value must be integer'.format(value,index,subIndex))
                            return
                        subIndex = subIndex+1
                else:
                    logging.warning('invalid size of sublist at index number {}. the size must be 9'.format(index))
                    return
                index = index+1
            self.info = info
        else:
            logging.warning('invalid size of list. the size must be either 9 or 81. please see README for more information')

    def getModifiable(self,grid):
        modifiable = []
        for r in self.row:
            for c in self.column:
                if(grid[r+c]==0):
                    modifiable.append(r+c)
        return modifiable

    """
    This is solving algorithm by using Depth First search.
    Algorithm has serveral search heuristics.
    The main goal is understanding the performance and limitation of each heuristic
    """
    def AlgorithmByDFS(self,method=1):
        if(method==1):
            return self.ABD_helper1(self.info.copy())
        if(method==2):
            return self.ABD_helper2(self.info.copy())
        elif(method==3):
            grid = self.info.copy()
            predict = {}
            for cell in self.getModifiable(grid):
                predict[cell] = [1,2,3,4,5,6,7,8,9]
            return self.ABD_helper3(grid,predict)

    """
    This heuristic is the most simple one. This eliminates numbers by checking
    its neighbor numbers row-wise, column-wise, and 3x3 size grid.
    The idea can be called as Naked Single.
    This will not be able to solve if the problem requires some Sudoku techniques
    """
    def ABD_helper1(self,grid):
        lst = self.getModifiable(grid)
        changeCount = 0
        for cell in lst:
            pos = [1,2,3,4,5,6,7,8,9]
            for c in self.check[cell]:
                for d in self.distinct[c]:
                    if(grid[d]!=0 and grid[d] in pos):
                        pos.remove(grid[d])
            if(len(pos)==1):
                grid[cell] = pos[0]
                self.tracking.append((cell,pos[0]))
                changeCount = changeCount+1
        if(changeCount==0):
            return grid
        else:
            return self.ABD_helper1(grid)

    """
    this heuristics use same method as ABD_helper1, but it 'guesses' a number of cell and
    check if the guess is right by using DFS. This guarantees there is a cell that eventually
    has no possible number exists if the guessed number is wrong.
    If it finds the dead cell, it tries with different number until it has no dead cell in the grid.
    This idea is basically a brute-force with constraint propagation. This may be a good solution
    if you just need a program solving problems, but it is not a good idea if you want to see
    the hardness of the problem.
    """
    def ABD_helper2(self,grid):
        self.tracking_grid.append(grid)
        lst = self.getModifiable(grid)
        changeCount = 0
        predict = {}
        minCell = None
        for cell in lst:
            pos = [1,2,3,4,5,6,7,8,9]
            for c in self.check[cell]:
                for d in self.distinct[c]:
                    if(grid[d]!=0 and grid[d] in pos):
                        pos.remove(grid[d])
            if(len(pos)==1):
                grid[cell] = pos[0]
                changeCount = changeCount+1
            elif(len(pos)==0):
                return grid
            else:
                if(minCell==None or len(predict[minCell])>len(pos)):
                    minCell = cell
                predict[cell] = pos
        if(changeCount==0):
            if(minCell!=None):
                for candidate in predict[minCell]:
                    temp = grid.copy()
                    temp[minCell] = candidate
                    self.tracking.append((minCell,candidate))
                    result = self.ABD_helper2(temp)
                    if(len(self.getModifiable(result))==0):
                        return result
            return grid
        else:
            return self.ABD_helper2(grid)

    def AlgorithmByModules(self):
        grid = self.ABM_Init()
        changed = True
        while(changed):
            count = 0
            count = count + self.ABM_NakedSingle(grid)
            count = count + self.ABM_NakedPair(grid)
            #count = count + self.ABM_InterSectionLock(grid)
            count = count + self.ABM_HiddenSingle(grid)
            if(count==0):
                changed = False
            else:
                self.ABM_List2Int(grid)
        return grid

    def ABM_Init(self):
        grid = self.info.copy()
        for key in grid: # this time, we use grid that unknown cells are already initialized with a list of possible numbers
            value = grid[key]
            if(grid[key]==0):
                grid[key] = [1,2,3,4,5,6,7,8,9]
        return grid


    def ABM_List2Int(self,grid):
        for key in grid:
            value = grid[key]
            if(type(value) is list and len(value)==1):
                grid[key] = value[0]
    
    def ABM_NakedSingle(self,grid):
        count = 0
        for key in grid:
            value = grid[key]
            if(type(value) is list):
                for c in self.check[key]:
                    for d in self.distinct[c]:
                        if(type(grid[d]) is not list and grid[d] in value):
                            count = count + 1
                            value.remove(grid[d])
        return count

    def ABM_NakedPair(self,grid):
        count = 0
        for d in self.distinct:
            pair = []
            for index,cell in enumerate(d):
                temp = grid[cell]
                if(type(temp) is list and len(temp)==2):
                    for i in range(index+1,len(d)):
                        if(temp==grid[d[i]]):
                            pair.append((cell,d[i]))
            if(pair):
                for first,second in pair:
                    for cell in d:
                        val = grid[cell]
                        if(type(val) is list and cell is not first and cell is not second):
                            for num in grid[first]:
                                if(num in val):
                                    count = count + 1
                                    val.remove(num)
        return count

    def ABM_HiddenSingle(self,grid):
        count = 0
        for d in self.distinct:
            unknown = []
            for cell in d:
                if(type(grid[cell]) is list):
                    unknown.append(cell)
            for cell in unknown:
                posVal = []
                for num in grid[cell]:
                    duplicated = False
                    for other in unknown:
                        if(other is not cell and num in grid[other]):
                            duplicated = True
                    if(not duplicated):
                        posVal.append(num)
                if(posVal):
                    count = count + 1
                    grid[cell] = posVal
        return count

    def ABM_InterSectionLock(self,grid):
        blocks = self.distinct[:9]
        rows = self.distinct[9:18]
        columns = self.distinct[18:]
        return 0

            


                    





#-----------------test-------------------#
def translate(raw):
    lst = []
    for r in raw:
        if(r=='.'):
            lst.append(0)
        else:
            lst.append(int(r))
    return lst

sudo = Sudoku()
testSudo0 = [
        [0,0,5,1,6,0,0,0,0],
        [6,0,0,0,7,3,0,0,0],
        [3,0,0,0,0,5,7,0,6],
        [0,0,0,0,3,0,6,9,1],
        [1,3,9,7,5,6,4,8,2],
        [8,6,2,4,9,1,0,0,7],
        [4,0,1,0,0,0,0,0,5],
        [0,0,0,5,0,0,0,0,8],
        [0,0,0,0,0,7,2,0,0]]
testSudo1 = [
        [0,0,8,5,6,0,2,0,0],
        [6,0,0,0,2,1,9,0,0],
        [7,2,0,0,0,3,0,6,4],
        [0,0,0,0,0,0,0,9,1],
        [0,4,0,0,0,0,0,3,0],
        [1,8,0,0,0,0,0,0,0],
        [9,7,0,6,0,0,0,5,2],
        [0,0,3,7,4,0,0,0,9],
        [0,0,6,0,1,2,3,0,0]]
testSudo2 = [9,0,0,0,0,5,1,0,0,0,0,0,4,0,0,0,0,3,0,4,0,0,0,0,8,2,5,3,8,4,0,0,0,0,0,2,0,0,0,0,7,0,0,0,0,7,0,0,0,0,0,4,6,9,8,6,1,0,0,0,0,5,0,5,0,0,0,0,6,0,0,0,0,0,3,5,0,0,0,0,8]
sudo.insert(testSudo2)
#sudo.insert(translate('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'))
#sudo.insert(translate('.....6....59.....82....8....45........3........6..3.54...325..6..................'))
#sudo.insert(translate('.....6....59.....82....8....45........3........6..3.54...325..6..................'))
sudo.insert(translate('7.91.3..553..6.........59.3.4...73.2.1....78.8.73...5...85.........4.836...6.85.7'))
sudo.print()
start = time.clock()
sudo.print(sudo.AlgorithmByDFS(2))
sudo.print(sudo.AlgorithmByModules())
print(time.clock()-start)
"""
for grid in sudo.tracking_grid:
    for _ in range(0,10):
        print("")
    sudo.print()
    sudo.print(grid)
    time.sleep(.01)

for key,val in sudo.tracking:
    for _ in range(0,30):
        print("")
    sudo.update(key,val)
    sudo.print()
    time.sleep(.01)
    """
