# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def graphSearch(problem,search):
    start_state = problem.getStartState()
    method = []
    if (search == "DFS"):
        Frontier = util.Stack()
        Frontier.push(start_state)
    elif (search == "BFS"):
        Frontier = util.Queue()
        Frontier.push(start_state)
    elif (search == "UCS"):
        Frontier = util.PriorityQueue()
        Frontier.push(start_state,0)
    
    Explored = dict()
    
    while not Frontier.isEmpty():
        if (search == "DFS" or search == "BFS"):
            Explored.update({start_state:None})
            node = Frontier.pop() #(state, state's node's parents state, parent to node's action)
            if problem.isGoalState(node):
                trace_back = Explored[node]  
                while not (trace_back == None): 
                    method.append(trace_back[1])
                    trace_back = Explored.get(trace_back[0])
                method.reverse()
                #print method
                #return ['East','East','South','South','West','West','West','South','South','East','East','East','West','West']
                return method
            chosen_node = problem.getSuccessors(node) #list of (successor,action,stepcost)
            for i in range(len(chosen_node)):
                if not(Explored.has_key(chosen_node[i][0])):
                    Frontier.push(chosen_node[i][0]) #(node state,node's parent(state,action,cost))
                    Explored.update({chosen_node[i][0]:(node,chosen_node[i][1])})
        elif (search == "UCS"):
            Explored.update({start_state:(None,None,0)})
            node = Frontier.pop() #(state)
            if problem.isGoalState(node): 
                trace_back = Explored[node] #(parents,action,cost til now)  
                while not (trace_back == (None,None,0)): 
                    method.append(trace_back[1])
                    trace_back = Explored.get(trace_back[0])
                    #print trace_back
                method.reverse()
                return method
            chosen_node = problem.getSuccessors(node) #list of (successor,action,stepcost)
            for i in range(len(chosen_node)):
                if not(Explored.has_key(chosen_node[i][0])):
                    Frontier.push(chosen_node[i][0],Explored[node][2]+chosen_node[i][2]) #(node state,cost until now)
                    Explored.update({chosen_node[i][0]:(node,chosen_node[i][1],chosen_node[i][2]+Explored[node][2])})
                else:
                    if (Explored[chosen_node[i][0]][2]>Explored[node][2]+chosen_node[i][2]):
                        Explored[chosen_node[i][0]]=(node,chosen_node[i][1],chosen_node[i][2]+Explored[node][2])
                        Frontier.update(chosen_node[i][0],chosen_node[i][2]+Explored[node][2])
    return util.raiseNotDefined()


            

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return graphSearch(problem,"DFS")
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    return graphSearch(problem,"BFS")
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    return graphSearch(problem,"UCS")
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    method = []
    Frontier = util.PriorityQueue()
    Frontier.push(start_state,heuristic(start_state,problem))
    Explored = dict()
    while not Frontier.isEmpty():
        Explored.update({start_state:(None,None,heuristic(start_state,problem)+0)})
        node = Frontier.pop() #(state)
        if problem.isGoalState(node): 
            trace_back = Explored[node] #(parents,action,f(x)=(x)+h(x))  
            while not (trace_back == (None,None,heuristic(start_state,problem))): 
                method.append(trace_back[1])
                trace_back = Explored.get(trace_back[0])
                #print trace_back
            method.reverse()
            return method
        chosen_node = problem.getSuccessors(node) #list of (successor,action,stepcost)
        for i in range(len(chosen_node)):
            if not(Explored.has_key(chosen_node[i][0])):
                Frontier.push(chosen_node[i][0],Explored[node][2]+chosen_node[i][2]+heuristic(chosen_node[i][0],problem)-heuristic(node,problem)) #(node state,cost until now)
                Explored.update({chosen_node[i][0]:(node,chosen_node[i][1],chosen_node[i][2]+Explored[node][2]+heuristic(chosen_node[i][0],problem)-heuristic(node,problem))})
            else:
                if (Explored[chosen_node[i][0]][2]>Explored[node][2]+chosen_node[i][2]+heuristic(chosen_node[i][0],problem)):
                    Explored[chosen_node[i][0]]=(node,chosen_node[i][1],chosen_node[i][2]+Explored[node][2]+heuristic(chosen_node[i][0],problem)-heuristic(node,problem))
                    Frontier.update(chosen_node[i][0],chosen_node[i][2]+Explored[node][2]+heuristic(chosen_node[i][0],problem)-heuristic(node,problem))
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
