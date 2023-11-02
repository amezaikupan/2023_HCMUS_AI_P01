# Create game state class to store: 
# agents position
# points
# in a state.
import helper

# TODO: Missing recorder function to pass to path (search.py)

class GameState():
    def __init__(self):
        # Pacman position = 0
        # Ghost position >= 1
        self.agentsPosition = {}
        self.points = 0
        self.numberOfFood = 0
        self.map = [[]]

    def initMap(self, inMap):
        self.map = inMap
        # TODO: convert map to contain interger value
        # TODO: update agents number (count ghosts + pacman)
        # TODO: update number of food

    def getPacmanState(self):
        return self.agentsPosition[0]
    
    def getGhostState(self):
        return self.agentsPosition[1:]
    
    def getNumberOfAgents(self):
        return len(self.agentsPosition)

    def getAgentsStates(self):
        return self.agentsPosition
    
    def isAbleToMove(self, position):
        if(position[0] >= len(self.map[0]) or 
           position[1] >= len(self.map) or
           self.map[position[0]][position[1]] == '1'):
            return 0
        return 1
    
    def getValidSuccessor(self, agentID = 0):
        possibleDirections = [(0,1), (0,-1), (1, 0), (-1, 0)]

        currentState = self.agentsPosition[agentID]
        agentSuccessors = []
        
        for direction in possibleDirections:
            newPosition = currentState[0] + direction[0], currentState[1] + direction[1]

            if self.isAbleToMove(newPosition):
                agentSuccessors.append(newPosition.copy())
        return agentSuccessors
    
    def getPoints(self):
        return self.points
    
    def getMap(self):
        return self.map
    
    def getNumberOfFood(self):
        return self.numberOfFood
    
    # def IsEnd():
    #     #TODO: to implement   
        
# Create pacman agents class
class MinimaxAgents():
    def __init__(self):
        # Set default index is Pacman's index
        self.index = 0 

        # Depth is 2 because we also taken account
        # the inital positioning of pacman and ghosts
        self.depth = 2
    
    def getVision(self, position : tuple, gameState : GameState):
        gameMap = gameState.getMap()
        if(self.index == 0):
            # position = gameState.getPacmanState()
            sideVision = 7 // 2

            startRow = max(position[0] - sideVision, 0)
            endRow = min(sideVision + position[0], len(gameMap[0]))
            startCol = max(position[1] - sideVision, 0)
            endCol = min(position[1] + sideVision, len(gameMap))

            visionMatrix = gameMap[startRow:endRow, startCol:endCol]

    def isFoodVisible(self, position : tuple, gameState : GameState):
        if(self.index == 0):
            pacmanVision = self.getVision(position, gameState)
            if(2 in pacmanVision):
                return True
        return False
    
    def isGhostVisible(self, position : tuple, gameState : GameState):
        if(self.index == 0):
            pacmanVision = self.getVision(position, gameState)
            if(3 in pacmanVision):
                return True
        return False
    
    def evaluate(self, gameState : GameState):
        if self.index == 0:
            # If pacman won
            if gameState.getNumberOfFood == 0:
                return 1, gameState.getPoints()
            
            # If pacman is eaten
            agentsPosition = gameState.getAgentsPosition()
            if agentsPosition[0] in agentsPosition[1:].keys():
                return 0, gameState.getPoints()      
        # If pacman is stuck and other advance stages
        # TODO: How to process pacman eating food??

    def getAction(self, gameState : GameState):
        # TODO: check terminal state  
        self.evaluate(gameState) 

        # Maximizing agent aka. pacman
        if self.index == 0:
            bestVal = 0
            bestPos = ()

            # TODO: what are the "child state" that pacman should consider

            # Get valid successor for pacman
            successors = gameState.getValidSuccessor()
            for successor in successors:
                value = 0

                if(self.isFoodVisible(successor, gameState)):
                    # TODO: Calculate distance to food to determine weight
                    # Add to value if can get closer to food
                    value += 100

                if(self.isGhostVisible(successor, gameState)):
                    # TODO: Calculate distance to ghost to determine weight
                    # Take from value if get closer to ghost
                    value -= 200

                # TODO: Ask sensei if this is wrong because minimax is recursive OMG
                # I think I'm a bit mistaken so let's email sensei tonight
                # No need for recursive search because pacman can only move
                # 1 position to 4 adjacent direction
                # value += self.minimax(depth + 1, gameState)
                bestVal = max(bestVal, value)
                if(bestVal == value):
                    bestPos = successor

            return bestPos, bestVal
        
        # Minimizing agents aka. Ghosts
        else:
            # Make decision for a Ghost
            pacmanPosition = gameState.getPacmanState()
            bestVal = 1000
            bestPos = ()

            # Get valid successor for ghost
            successors = gameState.getValidSuccessor(self.index)
            for successor in successors:
                value = 1000
                value -= helper.Measure.getDistanceBetween2Points(successor, pacmanPosition)            

                # TODO: Does number of food effect ghosts' decisions?
                # TODO: Ask sensei if this is wrong because minimax is recursive OMG
                # I think I'm a bit mistaken so let's email sensei tonight
                # No need for recursive search because pacman can only move
                # 1 position to 4 adjacent direction
                # value += self.minimax(depth + 1, gameState)
                bestVal = min(bestVal, value)
                if(bestVal == value):
                    bestPos = successor

            return bestPos, bestVal

