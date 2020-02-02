# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
from searchAgents import mazeDistance
import search
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        eva = 0
        x,y = newPos
        ghost_not_threat = 0
        food_o = currentGameState.getNumFood()
        food_n = successorGameState.getNumFood()
        lower_bd = currentGameState.getFood().width + currentGameState.getFood().height #bound for food be eaten
        distance_f = [manhattanDistance(newPos,food) for food in newFood.asList()]
        distance_g = []
        dis_ng = []
        for s in newGhostStates: 
              dis_g = manhattanDistance(newPos,s.getPosition())
              if dis_g < 3 : #<3 consideration
                if s.scaredTimer < 2: #avail ghost
                      distance_g.append(dis_g)
                      continue
              dis_ng.append(dis_g)
        if distance_f :
              eva = eva + lower_bd - min(distance_f)
        if distance_g : 
              eva = eva + min(distance_g) 
        if food_o != food_n :
              eva = eva + lower_bd*2
        return eva + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.max_node(gameState,1,0)
    def max_node (self, gameState, depth, agent_id):
          eva_max = float("-inf")
          next_act = Directions.STOP
          check = []
          actions = gameState.getLegalActions(agent_id)
          if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
          for action in actions:
                eva = self.min_node(gameState.generateSuccessor(agent_id,action), depth, agent_id+1)
                if eva > eva_max:
                      eva_max = eva
                      next_act = action
          if depth == 1:
                return next_act
          return eva_max

    def min_node (self, gameState, depth, agent_id):
          eva_min = float("inf")
          eva_tmp = float("inf")
          actions = gameState.getLegalActions(agent_id)
          if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState) 
          for action in actions:
                if agent_id + 1 == gameState.getNumAgents():
                    if depth == self.depth:
                        eva_tmp = self.evaluationFunction(gameState.generateSuccessor(agent_id,action)) 
                    else:
                        eva_tmp = self.max_node(gameState.generateSuccessor(agent_id,action),depth+1,0)
                else: 
                    eva_tmp = self.min_node(gameState.generateSuccessor(agent_id,action),depth,agent_id+1)
                eva_min = min(eva_min,eva_tmp)
          return eva_min
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max_node(gameState,1,0,float("-inf"),float("inf"))
    def max_node (self, gameState, depth, agent_id, alpha, beta):
          eva_max = float("-inf")
          next_act = Directions.STOP
          actions = gameState.getLegalActions(agent_id)
          if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
          for action in actions:
                eva = self.min_node(gameState.generateSuccessor(agent_id,action), depth, agent_id+1,alpha,beta)
                if eva > eva_max:
                      eva_max = eva
                      next_act = action
                if eva_max > beta:
                      return eva_max
                alpha = max(alpha, eva_max)
          if depth == 1:
                return next_act
          return eva_max

    def min_node (self, gameState, depth, agent_id, alpha, beta):
          eva_min = float("inf")
          eva_tmp = float("inf")
          actions = gameState.getLegalActions(agent_id)
          if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState) 
          for action in actions:
                if agent_id + 1 == gameState.getNumAgents():
                    if depth == self.depth:
                        eva_tmp = self.evaluationFunction(gameState.generateSuccessor(agent_id,action)) 
                    else:
                        eva_tmp = self.max_node(gameState.generateSuccessor(agent_id,action),depth+1,0, alpha, beta)
                else: 
                    eva_tmp = self.min_node(gameState.generateSuccessor(agent_id,action),depth,agent_id+1, alpha, beta)
                eva_min = min(eva_min,eva_tmp)
                if eva_min <= alpha:
                      return eva_min
                beta = min (beta, eva_min)
          return eva_min

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.max_node(gameState, 1, 0)
    def max_node (self, gameState, depth, agent_id):
          eva_max = float("-inf")
          next_act = Directions.STOP
          actions = gameState.getLegalActions(agent_id)
          if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
          for action in actions:
                eva = self.exp_node(gameState.generateSuccessor(agent_id,action), depth, agent_id+1)
                if eva > eva_max:
                      eva_max = eva
                      next_act = action
          if depth == 1:
                return next_act
          return eva_max

    def exp_node (self, gameState, depth, agent_id):
          eva_arr = []
          eva_tmp = float("inf")
          eva_min = float("inf")

          actions = gameState.getLegalActions(agent_id)
          if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState) 
          for action in actions:
                if agent_id + 1 == gameState.getNumAgents():
                    if depth == self.depth:
                        eva_tmp = self.evaluationFunction(gameState.generateSuccessor(agent_id,action)) 
                    else:
                        eva_tmp = self.max_node(gameState.generateSuccessor(agent_id,action),depth+1,0)
                else: 
                    eva_tmp = self.exp_node(gameState.generateSuccessor(agent_id,action),depth,agent_id+1)
                eva_arr.append(eva_tmp)
             
          average_eva = float(sum(eva_arr))/len(eva_arr)
          return average_eva      
         

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    x,y = currentGameState.getPacmanPosition() #pacman position
    food_list = currentGameState.getFood().asList() #food not eaten yet
    cap_list = currentGameState.getCapsules() #pellet not eaten yet
    ghost_states = currentGameState.getGhostStates() #ghost states
    lower_bd = currentGameState.getFood().width + currentGameState.getFood().height
    dis_f = [manhattanDistance((x,y),food) for food in food_list]
    dis_cap = [mazeDistance((x,y),cap,currentGameState) for cap in cap_list]
    dis_ghost_can_eat = []
    dis_ghost_escape = []
    eva = 0
    
    for ghost in ghost_states:
          distance_g = manhattanDistance((x,y),ghost.getPosition())
          if ghost.scaredTimer > 2 :
                dis_ghost_can_eat.append(distance_g)
          else:
                if distance_g < 4 :
                  dis_ghost_escape.append(distance_g)
    if dis_f:
        eva = eva + (lower_bd - min(dis_f))
    if dis_cap:
        eva = eva + 3*(lower_bd - min(dis_cap))
    if dis_ghost_can_eat:
        eva = eva + 2*(lower_bd - min(dis_ghost_can_eat))
    if dis_ghost_escape:
        eva = eva + 4*min(dis_ghost_escape) + (sum(dis_ghost_escape)/len(dis_ghost_escape))/2
    return eva + currentGameState.getScore()
# Abbreviation
better = betterEvaluationFunction

