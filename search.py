# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import heapq

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

class Node:
    ''' A tree node that contains state information
    Arguments
    state: (tuple of current state, action, cost)
    parent: parent node 
    '''
    def __init__(self, state, parent, problem, heuristic=nullHeuristic):
        self.state = state[0]
        self.action = state[1]
        self.cost = state[2]
        self.parent = parent
        if parent:
            self.g_score = parent.g_score + self.cost
        else:
            self.g_score = 0
        self.h_score = heuristic(self.state, problem)
        self.f_score = self.g_score + self.h_score
        
    def __eq__(self, other):
        ''' Compare nodes only by there state '''
        return self.state == other.state

def solution(node):
    ''' Trace back the path to get to this node from root '''        
    path = util.Queue()
    while node.parent:
        path.push(node.action)
        node = node.parent
    return path.list

def search(problem, dataStructure):
    ''' General search function for BFS and DFS
    Argument 
    dataStructure: queue (BFS) or stack (DFS)
    '''
    from game import Directions
    root = Node([problem.getStartState(), Directions.STOP, 0], None, problem)
    if problem.isGoalState(root.state):
        return solution(root)
    
    frontier = dataStructure()
    frontier.push(root)
    explored = set()
    
    while not frontier.isEmpty():
        current_node = frontier.pop()
        explored.add(current_node.state)
        successors = problem.getSuccessors(current_node.state)
        
        for successor in successors:
            successor = Node(successor, current_node, problem)
            if successor.state not in explored and successor not in frontier.list:
                # Check for goal before adding into list
                if problem.isGoalState(successor.state): 
                    return solution(successor)
                else:    
                    frontier.push(successor)

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  return search(problem, util.Stack)
  
def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  return search(problem, util.Queue)

def find_item_in_list(item, list):
    ''' Find the index of an item in list 
        Return None of not found
    ''' 
    n = len(list)
    for i in range(n):
        if item == list[i]:
            return i
    return None 

def searchWithPriority(problem, heuristic=nullHeuristic):
    ''' General search function with heuristic and priority queue '''
    from game import Directions
    root = Node([problem.getStartState(), Directions.STOP, 0], None, problem, heuristic=heuristic)
    frontier = util.PriorityQueue()
    frontier.push(root, root.f_score)
    explored = set()
    
    while not frontier.isEmpty():
        current_node = frontier.pop()
        # Check for goal when going out of the queue
        if problem.isGoalState(current_node.state):
            return solution(current_node)
        explored.add(current_node.state)
        successors = problem.getSuccessors(current_node.state)
        
        for successor in successors:
            successor = Node(successor, current_node, problem, heuristic=heuristic)
            nodes_in_frontier = [heap[1] for heap in frontier.heap] # List of states in frontier
            in_frontier = find_item_in_list(successor, nodes_in_frontier) # Index of successor in frontier
            if successor.state not in explored and not in_frontier:
                # Check for consistency
                if successor.h_score - successor.parent.h_score + 1 < 0:
                    raise ValueError('inconsistent heuristics')
                frontier.push(successor, successor.f_score)
            elif in_frontier:
                # If a node is already in frontier with higher cost,
                # update the frontier node to reflect shorter path
                repeated_node = nodes_in_frontier[in_frontier]      
                if repeated_node.g_score > successor.g_score:
                    frontier.heap[in_frontier] = frontier.heap[-1]
                    frontier.heap.pop()
                    heapq.heapify(frontier.heap)
                    frontier.push(successor, successor.f_score)

def uniformCostSearch(problem):
  "Search the node of least total cost first. "

  return searchWithPriority(problem)

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  
  return searchWithPriority(problem, heuristic)
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
