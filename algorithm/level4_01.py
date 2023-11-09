import numpy as np
import random

# Simple reflex agent

class Measure():
    def ManhattanDistance(point1, point2):
        distance = abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
        return distance
    
    def EuclidDistance(point1, point2):
        distance = ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
        return distance

class GameState():
    def __init__(self, pacmanPos, inMap):
        # Pacman position = index 0
        # Ghost position >= index 1
        self.agentsPosition = []
        # self.points = 0
        self.foodPosition = []
        self.map = [[]]
        self.initMap(pacmanPos, inMap)

    def initMap(self, pacmanPos, inMap):
        self.map = np.array(inMap)
        self.agentsPosition.append(pacmanPos)

        ghostCounter = 1
        foodCounter = 0
        for row in range(len(inMap)):
            for col in range(len(inMap[0])):
                if inMap[row][col] == 3:
                    self.agentsPosition.append((row, col))
                    ghostCounter += 1
                if inMap[row][col] == 2:
                    self.foodPosition.append((row, col))
                    foodCounter += 1

    def getPacmanState(self):
        return self.agentsPosition[0]
    
    def getGhostState(self):
        return self.agentsPosition[1:]
    
    def getNumberOfAgents(self):
        return len(self.agentsPosition)

    def getAgentsStates(self):
        return self.agentsPosition
    
    def isAbleToMove(self, position):
        if(position[0] >= len(self.map) or 
           position[0] < 0 or
           position[1] >= len(self.map[0]) or
           position[1] < 0 or
           self.map[position[0]][position[1]] == 1):
            return 0
        return 1
    
    def getValidSuccessor(self, position : tuple):
        possibleDirections = [(0,1), (0,-1), (1, 0), (-1, 0)]

        agentSuccessors = []
        for direction in possibleDirections:
            newPositionRow = position[0] + direction[0]
            newPositionCol = position[1] + direction[1]

            newPosition = (newPositionRow, newPositionCol)

            if self.isAbleToMove(newPosition):
                agentSuccessors.append(newPosition)
        return agentSuccessors
    
    def getPoints(self):
        return self.points
    
    def getMap(self):
        return self.map
    
    def getNumberOfFood(self):
        return len(self.foodPosition)
    
    def getFoodPositions(self):
        return self.foodPosition
    
    def updatePacmanState(self, newState):
        self.agentsPosition[0] = newState
    
    def updateGhostSate(self, newState, index):
        self.agentsPosition[index] = newState
    
    def updateMap(self, index : tuple, value):
        self.map[index[0]][index[1]] = value

    def updateFoodEaten(self, index : tuple):
        self.foodPosition.remove(index)

    def isWin(self):
        if self.getNumberOfFood() == 0:
            return True
        return False

    def isLose(self):
        if self.getPacmanState() in self.getGhostState():
            return True
        return False

class ReflexAgent():
    def __init__(self, index = 0):
        # Set default index is Pacman's index = 0
        self.index = index 
    
    def getVision(self, position : tuple, gameState : GameState):
        gameMap = gameState.getMap()
        if(self.index == 0):
            sideVision = 7

            startRow = max(position[0] - sideVision, 0)
            endRow = min(sideVision + position[0] + 1, gameMap.shape[0])
            startCol = max(position[1] - sideVision, 0)
            endCol = min(position[1] + sideVision + 1, gameMap.shape[1])

            return [startRow, endRow, startCol, endCol]
        

    def isFoodVisible(self, position : tuple, gameState : GameState):
        foodPositions = gameState.getFoodPositions()
        vision = self.getVision(position, gameState)
        visibleFoodPositions = []
        for foodPosition in foodPositions:
            if(foodPosition[0] >= vision[0] and foodPosition[0] <= vision[1] and
               foodPosition[1] >= vision[2] and foodPosition[1] <= vision[3]):
                visibleFoodPositions.append(foodPosition)
        
        return visibleFoodPositions
    
    def isGhostVisible(self, position : tuple, gameState : GameState):
        ghostPositions = gameState.getGhostState()
        vision = self.getVision(position, gameState)
        visibleGhostPositions = []
        for ghostPosition in ghostPositions:
            if(ghostPosition[0] >= vision[0] and ghostPosition[0] <= vision[1] and
               ghostPosition[1] >= vision[2] and ghostPosition[1] <= vision[3]):
                visibleGhostPositions.append(ghostPosition)
        
        return visibleGhostPositions
    
    def pacmanUtility(self, position : tuple, gameState: GameState):
        value = 1000
        foodWeight = 1.0
        visibleFoodPosition = self.isFoodVisible(position, gameState)
        foodDistance = []
        if(len(visibleFoodPosition) != 0):
            for food in visibleFoodPosition:
                foodDistance.append(Measure.EuclidDistance(food, position))
            value += foodWeight/(min(foodDistance) + 1e-1)
        visibleGhostPosition = self.isGhostVisible(position, gameState)
        
        if(len(visibleGhostPosition) != 0):
            ghostDistance = []
            for ghost in visibleGhostPosition:
                ghostDistance.append(Measure.ManhattanDistance(ghost, position))                           

            if min(ghostDistance) <= 1:
                return -9999
        return value

    def ghostUltility(self, position : tuple, gameState : GameState):
        value = 1000
        value += Measure.ManhattanDistance(position, gameState.getPacmanState())
        return value    

    def evaluate(self, postion : tuple, gameState : GameState):
        if gameState.isWin():
            return 100000
        elif gameState.isLose():
            return -99999    
        else:
            if self.index == 0:
                return self.pacmanUtility(postion, gameState)
            else:
                return self.ghostUltility(postion, gameState)

    def getAction(self, gameState : GameState, position, index):
        if index == 0:
            bestVal = float('-inf')
            bestPos = ()

            # Get valid successor for pacman
            successors = gameState.getValidSuccessor(position)
            actions = []

            for successor in successors:
                value = self.pacmanUtility(successor, gameState)
                bestVal = max(value, bestVal)
                actions.append((value, successor))

            bestActions = [pair[1] for pair in actions if pair[0] == bestVal]
            bestPos = random.choice(bestActions)
            return bestPos, bestVal

        else:
            bestVal = float('inf')
            value = bestVal
            bestPos = ()
            successors = gameState.getValidSuccessor(position)
            for successor in successors:   
                value = self.ghostUltility(successor, gameState)
                bestVal = min(bestVal, value)
                if(bestVal == value):
                    bestPos = successor
            return bestPos, bestVal

def run(pacmanPos, inMap):
   # Create State Map
    gameState = GameState(pacmanPos, inMap)

    pacman = ReflexAgent()
    ghosts = []

    pacmanPath = []
    ghostPath = [] 

    pacmanPath.append(gameState.getPacmanState())

    fistGhostPath = []
    for index in range(len(gameState.getGhostState())):
        ghosts.append(ReflexAgent(index + 1))
        fistGhostPath.append(gameState.getGhostState()[index])
    ghostPath.append(fistGhostPath)
    
    gameEndState = 0
    frame = 0

    # While run game
    while(True):
        frame += 1
        if frame == 500:
            break

        pacmanPos = gameState.getPacmanState()
        newPacmanPos = pacman.getAction(gameState, pacmanPos, 0)
        if(newPacmanPos[1] == {0 or 1}):
            gameEndState = newPacmanPos[0]
            break

        gameState.updatePacmanState(newPacmanPos[0])
        pacmanPath.append(newPacmanPos[0])

        # Process if pacman is dead
        if newPacmanPos[0] in gameState.getGhostState():
            break

        counter = 1
        newGhostPos = []
        currentGhostPath = []
        ghostsPos = gameState.getGhostState()    
        for ghost in ghosts:
            newGhostPos = ghost.getAction(gameState, ghostsPos[counter - 1], counter)
            gameState.updateGhostSate(newGhostPos[0], counter)
            currentGhostPath.append(newGhostPos[0])
            counter += 1
        ghostPath.append(currentGhostPath)
        
        # Process if pacman eat food
        if newPacmanPos[0] in gameState.getFoodPositions():
            # gameState.updateMap(newPacmanPos, 0)
            gameState.updateFoodEaten(newPacmanPos[0])

        # Process if pacman is dead
        if newPacmanPos[0] in gameState.getGhostState():
            break

        # Process if pacman won
        if len(gameState.getFoodPositions()) == 0:
            break

    print("Pacman Path:")
    print(pacmanPath)

    print("Ghost Path:")
    print(ghostPath)           
    
    return pacmanPath, ghostPath, gameEndState
        
