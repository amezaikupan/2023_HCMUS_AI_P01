# Create game state class to store: 
# agents position
# points
# in a state.
import helper
import numpy as np

# TODO: Missing recorder function to pass to path (search.py)
class GameState():
    def __init__(self, pacmanPos, inMap):
        # Pacman position = 0
        # Ghost position >= 1
        self.agentsPosition = []
        self.points = 0
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

        print("FOOD POSITION" + str(self.foodPosition))

    def getPacmanState(self):
        # print("Pacman state " + str(self.agentsPosition[0]))
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

        # currentState = self.agentsPosition[agentID]
        agentSuccessors = []
        
        for direction in possibleDirections:
            # print(position)

            newPositionRow = position[0] + direction[0]
            newPositionCol = position[1] + direction[1]

            newPosition = (newPositionRow, newPositionCol)

            if self.isAbleToMove(newPosition):
                # print("Success position row: " + str(newPositionCol) + " New position col: " + str(newPositionRow))
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
        print(self.foodPosition)
        print(index)
        self.foodPosition.remove(index)

    # def IsEnd():
    #     #TODO: to implement   
        
# Create pacman agents class
class MinimaxAgents():
    def __init__(self, index = 0):
        # Set default index is Pacman's index
        self.index = index 
        self.height = 2
    
    def getVision(self, position : tuple, gameState : GameState):
        gameMap = gameState.getMap()
        if(self.index == 0):
            # position = gameState.getPacmanState()
            sideVision = 7 // 2

            startRow = max(position[0] - sideVision, 0)
            endRow = min(sideVision + position[0] + 1, gameMap.shape[0])
            startCol = max(position[1] - sideVision, 0)
            endCol = min(position[1] + sideVision + 1, gameMap.shape[1])

            # print(gameMap)
            # print(str(startRow) + str(endRow) + str(startCol) + str(endCol))
            # visionMatrix = gameMap[startRow:endRow, startCol:endCol]
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
    
    # TODO: Reprogram!!!
    def isGhostVisible(self, position : tuple, gameState : GameState):
        ghostPositions = gameState.getGhostState()
        vision = self.getVision(position, gameState)
        visibleGhostPositions = []
        for ghostPosition in ghostPositions:
            if(ghostPosition[0] >= vision[0] and ghostPosition[0] <= vision[1] and
               ghostPosition[1] >= vision[2] and ghostPosition[1] <= vision[3]):
                visibleGhostPositions.append(ghostPosition)
        
        return visibleGhostPositions
    
    def evaluate(self, position, gameState : GameState, index):
        # if self.index == 0:
        #     # If pacman won
        #     if gameState.getNumberOfFood == 0:
        #         return 1, gameState.getPoints()
            
        #     # If pacman is eaten
        #     agentsPosition = gameState.getAgentsStates()
        #     if agentsPosition[0] in agentsPosition[1:]:
        #         return 0, gameState.getPoints()      
            
        # return -1
        # # If pacman is stuck and other advance stages
        # # TODO: How to process pacman eating food??

        if self.index == 0:
            value = -10000

            foodWeight = 1.0
            ghostWeight = -1.0
            visibleFoodPosition = self.isFoodVisible(position, gameState)
            if(len(visibleFoodPosition) != 0):
                # TODO: Calculate distance to food to determine weight
                # Add to value if can get closer to food
                for food in visibleFoodPosition:
                    value += helper.Measure.getDistanceBetween2Points(food, position) * foodWeight
                    
                # print("Food is visible")
                # value += 1000

            visibleGhostPosition = self.isGhostVisible(position, gameState)
            if(len(visibleGhostPosition) != 0):
                # TODO: Calculate distance to ghost to determine weight
                # Take from value if get closer to ghost
                for ghost in visibleGhostPosition:
                    value += helper.Measure.getDistanceBetween2Points(ghost, position) * ghostWeight
                # print("Ghost is visible")
                # value -= 100

            # print("VALUE: " + str(value) + str(position))

            return value

        else:
            value = 10000
            value += helper.Measure.getDistanceBetween2Points(position, gameState.getPacmanState())

            # print("GHOST VALUE: " + str(value))
            return value            





    def getAction(self, gameState : GameState, position, index, height = 0):
        # TODO: check terminal state  
        # eval = self.evaluate(gameState)
        # # print(eval)
        # if(eval == {1 or 0}):
        #     return eval    
        
        # check height
        if height == self.height:
            value = self.evaluate(position, gameState, index)
            # print("Get to leaf" + str(value))
            return position, value

        # Maximizing agent aka. pacman
        if index == 0:
            # print("INITIAL PACMAN POS" + str(position))
            bestVal = float('-inf')
            bestPos = ()

            # TODO: what are the "child state" that pacman should consider

            # Get valid successor for pacman
            successors = gameState.getValidSuccessor(position)
            # print("Get pacman successors: ")
            # print(successors)
            for successor in successors:
                # value = self.getAction()

                # if(self.isFoodVisible(successor, gameState)):
                #     # TODO: Calculate distance to food to determine weight
                #     # Add to value if can get closer to food
                #     value += 1000

                # if(self.isGhostVisible(successor, gameState)):
                #     # TODO: Calculate distance to ghost to determine weight
                #     # Take from value if get closer to ghost
                #     value -= 100


                # print("Point: ")

                value = self.getAction(gameState, successor, 0, height + 1)
                # print("ACESSING PACMAN VALUE: " + str(value))
                bestVal = max(value[1], bestVal)

                if(bestVal == value[1]):
                    bestPos = successor

            return bestPos, bestVal
        
        # Minimizing agents aka. Ghosts
        else:
            # Make decision for a Ghost
            bestVal = float('inf')
            bestPos = ()

            # Get valid successor for ghost
            successors = gameState.getValidSuccessor(position)
            for successor in successors:   

                # TODO: Does number of food effect ghosts' decisions?
                # TODO: Ask sensei if this is wrong because minimax is recursive OMG
                # I think I'm a bit mistaken so let's email sensei tonight
                # No need for recursive search because pacman can only move
                # 1 position to 4 adjacent direction
                # value += self.minimax(depth + 1, gameState)
                value = self.getAction(gameState,successor, index, height + 1)
                # print("GHOST VALUE: " + str(value))
                bestVal = min(bestVal, value[1])

                # print("BEST VAL" + str(bestVal))
                if(bestVal == value[1]):
                    bestPos = successor

            return bestPos, bestVal

def run(pacmanPos, inMap):
    # Create State Map
    gameState = GameState(pacmanPos, inMap)

    pacman = MinimaxAgents()
    ghosts = []

    pacmanPath = []
    ghostPath = [] 

    pacmanPath.append(gameState.getPacmanState())

    fistGhostPath = []
    for index in range(len(gameState.getGhostState())):
        ghosts.append(MinimaxAgents(index + 1))
        fistGhostPath.append(gameState.getGhostState()[index])
    ghostPath.append(fistGhostPath)
    
    gameEndState = 0

    # While run game
    while(True):
        pacmanPos = gameState.getPacmanState()
        newPacmanPos = pacman.getAction(gameState, pacmanPos, 0)
        if(newPacmanPos[1] == {0 or 1}):
            gameEndState = newPacmanPos[0]
            break

        gameState.updatePacmanState(newPacmanPos[0])
        pacmanPath.append(newPacmanPos[0])
        print("New pacman state: " + str(newPacmanPos))

        # Process if pacman is dead
        if newPacmanPos[0] in gameState.getGhostState():
            break

        counter = 1
        newGhostPos = []
        currentGhostPath = []
        ghostsPos = gameState.getGhostState()    
        for ghost in ghosts:
            newGhostPos = ghost.getAction(gameState, ghostsPos[counter - 1], counter)
            print("New ghost pos")
            print(newGhostPos)
            gameState.updateGhostSate(newGhostPos[0], counter)
            currentGhostPath.append(newGhostPos[0])
            counter += 1
        ghostPath.append(currentGhostPath)
        
        # Process if pacman eat food
        if newPacmanPos[0] in gameState.getFoodPositions():
            print("PACMAN EAT FOOD!")
            # gameState.updateMap(newPacmanPos, 0)
            gameState.updateFoodEaten(newPacmanPos[0])

        # Process if pacman is dead
        if newPacmanPos[0] in gameState.getGhostState():
            break

        # Process if pacman won
        if len(gameState.getFoodPositions()) == 0:
            print("PACMAN WIN")
            break

    print("Pacman Path:")
    print(pacmanPath)

    print("Ghost Path:")
    print(ghostPath)           
    return gameEndState, pacmanPath, ghostPath

mapTest = [[0,1,1,2,1,3],[0,0,0,0,0,0],[0,0,0,0,0,0]]
pacmanTestPos = 0,0
run(pacmanTestPos, mapTest)    
        
