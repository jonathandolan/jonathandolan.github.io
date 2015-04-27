"""
Python script that reads in a Sudoku puzzle.

Author: Chris Fowles

Usage:

    python SudokuSolver [ puzzle ] 
"""

import sys

'''
A class representing a Sudoku puzzle solver
'''

class SudokuSolver:

    def __init__(self):
        # set up the puzzle as a list of lists
        self.puzzle = [ ]

        # the size of the puzzle
        self.size = 0

    '''
    Read in the puzzle and set it up as a list of lists.
    '''

    def initializePuzzle(self, fileName):
        
        with open(fileName) as puzzle_file:
            for row in puzzle_file:
                self.puzzle.append(row.split())

        # establishes the size of the puzzle
        self.size = len(self.puzzle)

    def outputPuzzle(self):
        row = 0

        for row in range(self.size):
            print '[',row,']', self.puzzle[row]
            
    

    '''Calls solveSudoku with 0,0'''
    def solveIt(self):
        self.solveSudoku(i=0, j=0)
        
    '''Finds the next cell (from the current point) with a '*' that it has to fill'''        
    def nextCell(self, i, j):
        #From where we are
        for x in range(i,9):
            for y in range(j,9):
                if self.puzzle[x][y] is '*':
                    return x,y    
            for x in range(0,9):
                for y in range(0,9):
                    if self.puzzle[x][y] is '*':
                        return x,y
        return -1,-1 #Returns -1 if no more cells

    '''FORWARD CHECKING whether value is ok for row, column, and box'''
    def isValid(self, i, j, value):
        row = all([`value` != self.puzzle[i][x] for x in range(9)])
        if row:
                column = all([`value` != self.puzzle[x][j] for x in range(9)])
                if column:
                        #Now check in the 3x3 box
                        boxRow, boxCol = self.findBox(i, j)
                        for x in range(boxRow, boxRow+3):
                                for y in range(boxCol, boxCol+3):
                                        if self.puzzle[x][y] == `value`:
                                                return False
                        return True
        return False


    '''Gets the top left cell for the box, then we can add 3 for row and col'''
    def findBox(self, i, j):
        boxRow = 3 *(i/3) 
        boxCol = 3 *(j/3)
        return boxRow, boxCol
    
    '''
    Recursive Algorithm for solving the Sudoku
    Finds the next cell to fill, then checks each value from 1 to 9 to see if they are valid
    If none are valid then the current cell is undone
    '''
    def solveSudoku(self, i, j):
        i,j = self.nextCell(i, j)
        if i == -1:
                return True
        for value in range(1,10):
            if self.isValid(i,j,value):
                self.puzzle[i][j] = `value`  #adds value as a string
                if self.solveSudoku(i, j):   #Recursive call with nextCell 
                    return True
                #BACKTRACKING
                self.puzzle[i][j] = '*'
        return False
    
    def printType(self):
        for i in self.puzzle:
            for j in i:
                print type(i)
                print type(j)

def main():
   
    solver = SudokuSolver()

    puzzle = sys.argv[1]    
  
    solver.initializePuzzle(puzzle)
    solver.outputPuzzle() 

    '''Solve the Sudoku starting at 0,0'''
    solver.solveIt()
    solver.outputPuzzle()


if __name__ == "__main__":
    
    # some preliminary error checking
    
    if len(sys.argv) != 2:
        print 'Usage: python SudokuSolver.py [ puzzle ]'
    else:
        main()