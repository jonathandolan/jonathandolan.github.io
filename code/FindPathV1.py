"""
Python script that reads in a graph with specified starting and goal states.

The objective is to design search algorithms that find a path from the start
to gaol state. Algorithms include:

Author: Jonathan Dolan

(1) Depth-frist search
(2) Breadth-first search
(3) uniform cost search
(4) A* search

Usage:

    python FindPathV1 [ maze ] [ astar | ucs | bfs | dfs ]
"""

import sys
import heapq
import time

'''
A class representing a search problem
'''

class SearchProblem:

    def __init__(self):
        self.startState = None
        self.goalState = None
        self.numberOfRows = 0
        self.numberOfColumns = 0
        self.mazeAsDictionary = { }
    
    '''
    Reads in the maze and returns a dictionary that maps
    the maze as a dictionary.
    '''

    def initializeMaze(self, fileName):
        
        self.fileName = fileName
        
        with open(fileName) as maze:
            row = 0
            for line in maze:
                for col in range(0,len(line)-1):
                    # set up the dictionary
                    self.mazeAsDictionary[(row,col)] = line[col]
            
                    # determine the start and goal states
                    if line[col] == 'S':
                        self.startState = (row,col)
                    if line[col] == 'G':
                        self.goalState = (row,col)
        
                row += 1

        # set the number of rows and columns in the maze
        self.numberOfRows = row - 1
        self.numberOfColumns = col

        return self.mazeAsDictionary


    '''
    returns a list of successors we can reach
    from the current state
    '''
    def getSuccessors(self):
        
        mazeWithSuccessors = { }

        for (currentRow, currentCol) in self.mazeAsDictionary.keys():
            # where can we go?
    
            successors = []
            nextState = ()
            
            # check NORTH
            if currentRow > 0:
                rowAbove = currentRow - 1
     
                if self.mazeAsDictionary[(rowAbove,currentCol)] != '%':
                    direction = 'NORTH'
                    nextState = (rowAbove,currentCol)

                    cost = getCost(rowAbove, currentCol)
        
                    successors.append( (cost, nextState, direction) )
                    
                                # check EAST
            if currentCol < self.numberOfColumns:
                columnToTheRight = currentCol + 1
    
                if self.mazeAsDictionary[(currentRow, columnToTheRight)] != '%':
                    direction = 'EAST'
                    nextState = (currentRow, columnToTheRight)
                    
                    cost = getCost(currentRow, columnToTheRight)

                    successors.append( (cost, nextState, direction) )
            # check SOUTH
            if currentRow < self.numberOfRows:
                rowBelow = currentRow + 1
                
                if self.mazeAsDictionary[(rowBelow,currentCol)] != '%':
                    direction = 'SOUTH'
                    nextState = (rowBelow,currentCol)

                    cost = getCost(rowBelow, currentCol)

                    successors.append( (cost, nextState, direction) )
                    
            # check WEST
            if currentCol > 0:
                columnToTheLeft = currentCol - 1
        
                if self.mazeAsDictionary[(currentRow, columnToTheLeft)] != '%':
                    direction =  'WEST'
                    nextState = (currentRow, columnToTheLeft)

                    cost = getCost(currentRow, columnToTheLeft)

                    successors.append( (cost, nextState, direction) )


 
            # check SOUTH
            if currentRow < self.numberOfRows:
                rowBelow = currentRow + 1
                
                if self.mazeAsDictionary[(rowBelow,currentCol)] != '%':
                    direction = 'SOUTH'
                    nextState = (rowBelow,currentCol)

                    cost = getCost(rowBelow, currentCol)

                    successors.append( (cost, nextState, direction) )

           

            '''
            we only need to populate if there are successors 
            from (currentRow,currentState)
            '''
            if successors:
                mazeWithSuccessors[(currentRow, currentCol)] = successors

        return mazeWithSuccessors

    '''
    Returns the start state
    '''
    def getStartState(self):
        return self.startState

    '''
    Returns the goal state
    '''
    def getGoalState(self):
        return self.goalState

    """
    UGLY ..... but it works.
    
    This function is passed a list of states and outputs
    the path taken from the starting state to goal state

    states is a list containing (row,column) tuples
    """
    def reportGraph(self, states):
        if states == None:
            return

        rows = [ ]
        
        with open(self.fileName) as maze:
            for line in maze:
                row = []
                for c in line[:-1]:
                    row.append(c)
                rows.append(row)
    
        # highlight each state that is along the path
        for (row,col) in states:
            rows[row][col] = '.'

        # ensure start and goal states are identified
        (startRow, startColumn) = self.startState
        rows[startRow][startColumn] = 'S'
        (goalRow, goalColumn) = self.goalState
        rows[goalRow][goalColumn] = 'G'

        # output the maze with the path
        for row in rows:
            print "".join(row)

"""
This represents a node in the search tree
"""
class Node:
    """
    pathCost    - the cost of reaching this node from the starting node
    state       - the state (row,col)
    direction   - the direction we came from
    parent      - the parent of this node
    """
    def __init__(self, pathCost, state, direction = None, parent = None):
        self.state = state
        self.direction = direction
        self.parent = parent
        
        if parent:
            self.pathCost = parent.pathCost + pathCost
        else:
            self.pathCost = pathCost


'''
determine the cost of reaching this (row,col) state
'''
def getCost(row,col):
    '''
    Very simple stepwise cost
    '''

    cost = 1

    return cost

"""
the heuristic for a-star search algorithm.
   
(point1, point2) are tuples of type (row,col)
 
this can be any admisssable heuristic such
as the Manhattan distance between the pair of points
"""
def heuristic(point1, point2):
    # use the following Manhattan heuristic for a-star and uniform cost
    distance = abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


    return distance

'''
A-Star search algorithm.
'''
def astar(problem, maze):
    print 'A*'
    startTime = time.clock()
    problem.initializeMaze(maze)
    node = Node(0, problem.getStartState()) 
    mazeWithSuccessors = problem.getSuccessors()
    frontier = []
    explored = set()
    states = list()
    
    heapq.heappush(frontier, (node.pathCost + heuristic(node.state, problem.getGoalState()), node))
   
    while frontier:
        #remove node from frontier
        (tempHeur, node) = heapq.heappop(frontier)
        if node.state == problem.getGoalState():
            print node.pathCost
            #states = path from start to node
            while node.state != problem.getStartState():
                parentNode = node.parent
                states.append(parentNode.state)
                node = parentNode
            break
        
        if node.state not in explored:
            explored.add(node.state)
            #add successors to frontier
            for (s1,s2, s3) in mazeWithSuccessors[node.state]: 
                heapq.heappush(frontier, (node.pathCost + heuristic(node.state, problem.getGoalState()), Node(s1, s2, s3, node)))

    print "time to complete"
    print time.clock() - startTime
    return states

'''
uniform cost search
'''
def ucs(problem, maze):
    print 'UCS'
    startTime = time.clock()
    problem.initializeMaze(maze)
    node = Node(0, problem.getStartState()) 
    mazeWithSuccessors = problem.getSuccessors()
    frontier = []
    explored = set()
    states = list()
    
    heapq.heappush(frontier, (heuristic(node.state, problem.getGoalState()), node))
   
    while frontier:
        #remove node from frontier
        (tempHeur, node) = heapq.heappop(frontier)
        if node.state == problem.getGoalState():
            print node.pathCost
            #states = path from start to node
            while node.state != problem.getStartState():
                parentNode = node.parent
                states.append(parentNode.state)
                node = parentNode
            break
        
        if node.state not in explored:
            explored.add(node.state)
            #add successors to frontier
            for (s1,s2, s3) in mazeWithSuccessors[node.state]: 
                heapq.heappush(frontier, (heuristic(node.state, problem.getGoalState()), Node(s1, s2, s3, node)))

    print "time to complete"
    print time.clock() - startTime
    return states

'''
bradth-first search
'''
def bfs(problem, maze):
    print 'BFS'
    startTime = time.clock()
    '''
    This demonstrates how to initialize the maze
    '''
    problem.initializeMaze(maze)

    '''
    This generates the successors in the maze.
    This is a direction with [key:value] pairs
    being [state:(list of adjacent states)]
    '''
    
  
    node = Node(0, problem.getStartState())
    
    mazeWithSuccessors = problem.getSuccessors()
    frontier = []
    frontier.append(node)

    explored = set()
    
    states = list()

    while frontier:
        #remove node from frontier
        node = frontier.pop(0)
        if node.state == problem.getGoalState():
            print node.pathCost
            #states = path from start to node
            while node.state != problem.getStartState():
                parentNode = node.parent
                states.append(parentNode.state)
                node = parentNode
            break
        
        if node.state not in explored:
            explored.add(node.state)
            #add successors to frontier
            for (s1,s2, s3) in mazeWithSuccessors[node.state]: 
                frontier.append(Node(s1, s2, s3, node))
    
    print "time to complete"
    print time.clock() - startTime
    return states

'''
depth-first search
'''
def dfs(problem, maze):
    print 'DFS'
    startTime = time.clock()
    problem.initializeMaze(maze)

    '''
    This generates the successors in the maze.
    This is a direction with [key:value] pairs
    being [state:(list of adjacent states)]
    '''
    
    node = Node(0, problem.getStartState())
    
    mazeWithSuccessors = problem.getSuccessors()
    frontier = []
    frontier.append(node)

    explored = set()
    
    states = list()

    while frontier:
        #remove node from frontier
        node = frontier.pop()
        if node.state == problem.getGoalState():
            print node.pathCost
            #states = path from start to node
            while node.state != problem.getStartState():
                parentNode = node.parent
                states.append(parentNode.state)
                node = parentNode
            break
        
        if node.state not in explored:
            explored.add(node.state)
            #add successors to frontier
            for (s1,s2, s3) in mazeWithSuccessors[node.state]: 
                    frontier.append(Node(s1, s2, s3, node))
    print "time to complete"
    print time.clock() - startTime
    return states

'''
Invokes the appropriate search algorithm.
'''
def searchStrategy(problem, maze, algorithm):
    if algorithm == 'astar':
        return astar(problem, maze)
    elif algorithm == 'ucs':
        return ucs(problem, maze)
    elif algorithm == 'bfs':
        return bfs(problem, maze)
    elif algorithm == 'dfs':
        return dfs(problem, maze)
    else:
        return 'Error: Unimplemented Algorithm'

def main():
   
    problem = SearchProblem()

    maze = sys.argv[1]    
    algorithm = sys.argv[2]
   
    problem.reportGraph( searchStrategy(problem, maze, algorithm) )


if __name__ == "__main__":
    
    # some preliminary error checking
    
    if len(sys.argv) != 3:
        print 'Usage: python FindPath.py [maze] [dfs | bfs | astar | ucs]'
    elif sys.argv[2] == 'bfs' or sys.argv[2] == 'dfs' or sys.argv[2] == 'ucs' or sys.argv[2] == 'astar': 
        main()
    else:
        print 'Invalid algorihm: Must be [dfs | bfs | ucs | astar'
