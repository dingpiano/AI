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
        newNumFood = successorGameState.getNumFood()
        curNumFood = currentGameState.getNumFood()
        curPowerPelletPos = currentGameState.getCapsules()
        ghostPos = currentGameState.getGhostPosition(1)
        ghostDis = util.manhattanDistance(ghostPos, newPos)
        closestFoodDis = 999999999
        score = 0
        
        #return a high score immediately if the next move wins and concludes the game
        if successorGameState.isWin():
            return 99999999999999999
        
        #if succesor state has fewer food (i.e. food eaten), increase score
        if (curNumFood > newNumFood): 
            score += 100
            
        #further away the ghosts are, the better
        score += ghostDis 

        #encourage eating a power pellet
        if successorGameState.getPacmanPosition() in curPowerPelletPos:
            score += 150
            
        #encourage eating ghosts only when Pacman has at least three moves (cautious to leave time to run)
        #also only when ghost is closeby (as eating ghosts won't win the game, so don't lose track of the purpose of eating food)
        if (ghostDis < 5)  and (newScaredTimes[0] >= 3):
            score += 150
        
        #not on power pellet, so try to stay at least 3 steps away from ghost
        if (ghostDis <= 3) and (newScaredTimes[0] == 0):	
            score -= 9999999
            
        #discourage staying still, as ghost will not be staying still, so gap will only be closing
        if action == Directions.STOP:
            score -= 1000
            
        #encourage being close to the closest food, by subtracting 5*closest food distance from score
        #this is disfavour having far away foods (technically far away closest food)
        for food in newFood.asList():
            foodDis = util.manhattanDistance(food, newPos)	
            if (closestFoodDis >= foodDis): 
                closestFoodDis = foodDis
                
        score -= 5 * closestFoodDis
            
        return successorGameState.getScore() + score


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
        #All of Pacman's legal actions
        newState=[]
        legalMoves=gameState.getLegalActions(0)
        for action in legalMoves:
            newState.append(gameState.generateSuccessor(0,action))
    	
        #after Pacman has made the move,, time for Ghosts' evaluations, so use Min of minimax
        #startin with ghost 1
        scores=[]
        bestIndices=[]
        for state in newState:
            scores.append(self.minimax("Min", state, 0, 1))
        bestScore = max(scores) #Pacman is a Max agent, so Pacman will choose the maximum score
        for index in range(len(scores)):
            if bestScore == scores[index]: #find all indices whose score is equal to the best score
                bestIndices.append(index)
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best, from Reflex code provided
        return legalMoves[chosenIndex] #this is the state with the maximum value for Pacman
    
    #minimax function follows the minimax algorithm peusdocode given in the lecture-3 Games.pdf
    def minimax(self, player, gameState, curDepth, agentIndex=1):
        if(self.depth==curDepth or gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)   
        if player == "Max":
            legalMoves=gameState.getLegalActions(0) #Pacman's legal moves
            newState=[]
            scores=[]
            for action in legalMoves:
                newState.append(gameState.generateSuccessor(0,action)) #sucessor states following Pacman's move
            for state in newState:
                scores.append(self.minimax("Min", state, curDepth, 1)) #same depth, as each depth has Pacman + # of ghosts levels
            return max(scores) #Pacman takes the highest score
        elif player == "Min":
            legalMoves=gameState.getLegalActions(agentIndex) #Ghost[agentIndex]'s legal moves
            newState=[]
            scores=[]
            for action in legalMoves:
                newState.append(gameState.generateSuccessor(agentIndex, action)) #successor states following ghost's move
            for state in newState:
                if(agentIndex==(gameState.getNumAgents()-1)): #if all ghosts checked, no need to further increase agentIndex
                    scores.append(self.minimax("Max", state, curDepth+1)) #increase depth, back to Pacman
                else:
                    scores.append(self.minimax("Min", state, curDepth, agentIndex+1)) #same depth, calculating next ghost - multiple levels within same depth
            return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        maxValue = -9999999999999999999999999999999999
        alpha = -9999999999999999999999999999999999
        beta = 9999999999999999999999999999999999
        legalMoves=gameState.getLegalActions(0) #Pacman's legal moves
        bestAction = Directions.STOP
        
        for action in legalMoves:
            newState = gameState.generateSuccessor(0, action)
            newValue = self.alphabeta("Min", newState, 0, 1, alpha, beta) #ghosts' moves
            if newValue > maxValue:
                maxValue = newValue
                bestAction = action
            alpha = max(alpha, maxValue) #selecting the max option as Pacma is a max player
        return bestAction
        
    #alphabeta function follows the alphabeta pruning algorithm peusdocode given in the lecture-3 Games.pdf
    def alphabeta(self, player, gameState, curDepth, agentIndex, alpha, beta):
        if(self.depth==curDepth or gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        
        elif player == "Max":
            maxValue = -9999999999999999999999999999999999
            for action in gameState.getLegalActions(0):
                maxValue = max(maxValue, self.alphabeta("Min", gameState.generateSuccessor(0, action), curDepth, 1, alpha, beta)) 
                if maxValue >= beta:
                    return maxValue #immediately return maxValue and prune branches
                alpha = max(alpha, maxValue)
            return maxValue
        
        elif player == "Min": 
            minValue = 9999999999999999999999999999999999
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == (gameState.getNumAgents()-1): #end of ghosts, go to next depth level and switch to Pacman
                    minValue = min(minValue, self.alphabeta("Max", gameState.generateSuccessor(agentIndex, action), curDepth+1, 0, alpha, beta))
                if agentIndex != (gameState.getNumAgents()-1): #continue onto next ghost (i.e. increase level, but not search depth)
                    minValue = min(minValue, self.alphabeta("Min", gameState.generateSuccessor(agentIndex, action), curDepth, agentIndex+1, alpha, beta))
                if minValue <= alpha:
                    return minValue #immediately return minValue and prune branches
                beta = min(beta, minValue)
        return minValue

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
        
        maxValue = -9999999999999999999999999999999999
        legalMoves=gameState.getLegalActions(0) #Pacman's legal moves
        bestAction = Directions.STOP
        for action in legalMoves:
            newState = gameState.generateSuccessor(0, action) #ghosts' moves
            newValue = self.expectimax("Min", newState, 0, 1) #run expectimax on ghosts
            if newValue > maxValue: 
                maxValue = newValue
                bestAction = action #best action for pacman is the largest score out of all ghosts moves
        return bestAction
    
    def expectimax(self, player, gameState, curDepth, agentIndex):
        if curDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        elif player == "Max": #regular returning max for Pacman
            maxValue = -9999999999999999999999999999999999
            for action in gameState.getLegalActions(0):
                maxValue = max(maxValue, self.expectimax("Min", gameState.generateSuccessor(0, action), curDepth, 1))
            return maxValue
        
        elif player == "Min": #for ghosts return the average value
            avgValue = 0
            prob_length = float(len(gameState.getLegalActions(agentIndex))) #this is the denominator
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == (gameState.getNumAgents()-1):
                    avgValue = avgValue + float(self.expectimax("Max", gameState.generateSuccessor(agentIndex, action), curDepth+1, 0))/prob_length
                else:
                    avgValue = avgValue + float(self.expectimax("Min", gameState.generateSuccessor(agentIndex, action), curDepth, agentIndex+1))/prob_length
        return avgValue
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    curGameScore = currentGameState.getScore()
    numFood = currentGameState.getNumFood()
    curGhostStates = currentGameState.getGhostStates()
    pacmanPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    foodsPos = curFood.asList()
    foodsPos = sorted(foodsPos, key = lambda food: manhattanDistance(pacmanPos, food)) #sort by distance from pacman to food
    
    closestFoodDis = 0

    if len(foodsPos) > 0:
        closestFoodDis = manhattanDistance(foodsPos[0], pacmanPos) #finding the closest food pellet from current pacman position

    #assigning a score depending on the ghosts' current states
    closestGhostDis = 9999999999999999999999999999999999
    ghostScore = 0
    for ghost in curGhostStates:
        ghostPos = ghost.getPosition()
        curGhostDis = manhattanDistance(pacmanPos, ghostPos)
        if ghost.scaredTimer == 0 and curGhostDis < closestGhostDis:
            closestGhostDis = curGhostDis #find the closest ghost
        elif ghost.scaredTimer > curGhostDis:
            ghostScore += 200 - curGhostDis #updated score immediately for all ghosts if pacman is on power pellet
      
    if closestGhostDis == 9999999999999999999999999999999999:
      closestGhostDis = 0
    ghostScore += closestGhostDis
    
    return curGameScore + ghostScore - (2*closestFoodDis) - (5*numFood)
    #ghostScore encourages being far away from the closest ghost
    #want to be close to food pellets (closestFoodDis lower the better)
    #want to be eating food (numFood lower the better)

# Abbreviation
better = betterEvaluationFunction

